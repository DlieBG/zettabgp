from src.models.mrt_library import MRTScenarioRequest, MRTScenarioResult, MRTScenario, MRTLibrary
from src.parsers.mrt_bgp4mp import MrtBgp4MpParser
from src.adapters.rabbitmq import RabbitMQAdapter
from src.adapters.mongodb import MongoDBAdapter
from src.models.route_update import ChangeType
from fastapi.exceptions import HTTPException
from datetime import datetime
from fastapi import APIRouter
from mrtparse import Reader
from pathlib import Path
import json, time, os

mrt_library_router = APIRouter()

def _get_mrt_library() -> MRTLibrary:
    mrt_library = MRTLibrary(
        scenarios=[],
    )

    for scenario_file in Path(
        os.getenv('ZETTABGP_WEBAPP_MRT_LIBRARY_PATH', 'src/mrt_library')
    ).glob('**/scenario.json'):
        with open(scenario_file, 'r') as file:
            scenario = json.loads(file.read())
            scenario['id'] = str(scenario_file.parent.absolute()).replace('/', '-')
            scenario['path'] = str(scenario_file.parent.absolute())

            mrt_library.scenarios.append(
                MRTScenario.model_validate(
                    obj=scenario,
                )
            )

    return mrt_library

def _get_mrt_scenario(id: str) -> MRTScenario:
    for scenario in _get_mrt_library().scenarios:
        if scenario.id == id:
            return scenario

@mrt_library_router.get('/')
def get_mrt_library() -> MRTLibrary:
    return _get_mrt_library()

@mrt_library_router.post('/')
def start_mrt_scenario(mrt_scenario_request: MRTScenarioRequest) -> MRTScenarioResult:
    scenario = _get_mrt_scenario(
        id=mrt_scenario_request.id,
    )

    if not scenario:
        return HTTPException(
            status_code=400,
            detail='Scenario not found.',
        )

    mrt_scenario_result = MRTScenarioResult(
        count_announce=0,
        count_withdraw=0,
    )

    parser = MrtBgp4MpParser()

    if not scenario.no_rabbitmq_direct or scenario.rabbitmq_grouped:
        RabbitMQAdapter(
            parser=parser,
            no_direct=scenario.no_rabbitmq_direct,
            queue_interval=scenario.rabbitmq_grouped,
        )

    if not scenario.no_mongodb_log or not scenario.no_mongodb_state or not scenario.no_mongodb_statistics:
        MongoDBAdapter(
            parser=parser,
            no_mongodb_log=scenario.no_mongodb_log,
            no_mongodb_state=scenario.no_mongodb_state,
            no_mongodb_statistics=scenario.no_mongodb_statistics,
            clear_mongodb=scenario.clear_mongodb,
        )

    playback_speed_reference: datetime = None

    for mrt_file in scenario.mrt_files:
        mrt_file = str(Path(scenario.path) / Path(mrt_file))

        for message in Reader(mrt_file):
            if message.data['type'] != {16: 'BGP4MP'}:
                print('[dark_orange]\[WARN][/] Skipping unsupported MRT type: ', end='')
                print(message.data['type'])
                continue

            current_timestamp: datetime = datetime.fromtimestamp(
                timestamp=list(message.data['timestamp'].keys())[0],
            )

            if scenario.playback_speed:
                if playback_speed_reference:
                    time.sleep((current_timestamp - playback_speed_reference).seconds / scenario.playback_speed)

                playback_speed_reference = current_timestamp

            updates = parser.parse(
                bgp4mp_message=message,
            )

            if updates:
                for update in updates:
                    match update.change_type:
                        case ChangeType.ANNOUNCE:
                            mrt_scenario_result.count_announce += 1
                        case ChangeType.WITHDRAW:
                            mrt_scenario_result.count_withdraw += 1

    return mrt_scenario_result
