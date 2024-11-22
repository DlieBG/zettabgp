# -*- coding: utf-8 -*-
'''
ZettaBGP - Advanced Anomaly Detection in Internet Routing
Copyright (c) 2024 Benedikt Schwering and Sebastian Forstner

This work is licensed under the terms of the MIT license.
For a copy, see LICENSE in the project root.

Author:
    Benedikt Schwering <bes9584@thi.de>
    Sebastian Forstner <sef9869@thi.de>
'''
from src.models.mrt_library import MRTScenarioRequest, MRTScenarioResult, MRTScenario, MRTLibrary
from src.services.mrt_simulation import mrt_simulation
from fastapi import APIRouter, HTTPException
from pathlib import Path
import json, os

mrt_library_router = APIRouter()

def _get_mrt_library() -> MRTLibrary:
    '''
    This function returns the MRT library.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Returns:
        MRTLibrary: The MRT library.
    '''
    mrt_library = MRTLibrary(
        scenarios=[],
    )

    for scenario_file in Path(
        os.getenv('ZETTABGP_WEBAPP_MRT_LIBRARY_PATH', 'mrt_library')
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
    '''
    This function returns an MRT scenario by its ID.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Args:
        id (str): The ID of the MRT scenario.

    Returns:
        MRTScenario: The MRT scenario.
    '''
    for scenario in _get_mrt_library().scenarios:
        if scenario.id == id:
            return scenario

@mrt_library_router.get('/')
def get_mrt_library() -> MRTLibrary:
    '''
    This function returns the MRT library.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Returns:
        MRTLibrary: The MRT library.
    '''
    return _get_mrt_library()

@mrt_library_router.post('/')
def start_mrt_scenario(mrt_scenario_request: MRTScenarioRequest) -> MRTScenarioResult:
    '''
    This function starts an MRT scenario.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Args:
        mrt_scenario_request (MRTScenarioRequest): The MRT scenario request.

    Returns:
        MRTScenarioResult: The MRT scenario result.
    '''
    scenario = _get_mrt_scenario(
        id=mrt_scenario_request.id,
    )

    if not scenario:
        raise HTTPException(
            status_code=400,
            detail='Scenario not found.',
        )

    mrt_simulation_result = mrt_simulation(
        no_rabbitmq_direct=scenario.no_rabbitmq_direct,
        rabbitmq_grouped=scenario.rabbitmq_grouped,
        no_mongodb_log=scenario.no_mongodb_log,
        no_mongodb_state=scenario.no_mongodb_state,
        no_mongodb_statistics=scenario.no_mongodb_statistics,
        clear_mongodb=scenario.clear_mongodb,
        playback_speed=scenario.playback_speed,
        mrt_files=tuple([
            str(Path(scenario.path) / Path(mrt_file))
                for mrt_file in scenario.mrt_files
        ]),
    )

    return MRTScenarioResult(
        count_announce=mrt_simulation_result.count_announce,
        count_withdraw=mrt_simulation_result.count_withdraw,
    )
