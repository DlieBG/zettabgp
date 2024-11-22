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
from src.parsers.mrt_bgp4mp import MrtBgp4MpParser
from src.adapters.rabbitmq import RabbitMQAdapter
from src.adapters.mongodb import MongoDBAdapter
from src.models.route_update import ChangeType
from datetime import timedelta, datetime
from pydantic import BaseModel
from mrtparse import Reader
import time

class MRTSimulationResult(BaseModel):
    count_announce: int
    count_withdraw: int

def mrt_simulation(no_rabbitmq_direct: bool = False, rabbitmq_grouped: int = None, no_mongodb_log: bool = False, no_mongodb_state: bool = False, no_mongodb_statistics: bool = False, clear_mongodb: bool = False, playback_speed: int = None, playback_interval: int = None, mrt_files: tuple[str, ...] = ()) -> MRTSimulationResult:
    '''
    MRT Simulation service for retrieving BGP messages from MRT files and processing them.

    Author:
        Benedikt Schwering <bes9584@thi.de>
        Sebastian Forstner <sef9869@thi.de>

    Args:
        no_rabbitmq_direct (bool): Disable direct RabbitMQ direct queue..
        rabbitmq_grouped (int): Queue group interval in minutes.
        no_mongodb_log (bool): Disable logging to MongoDB.
        no_mongodb_state (bool): Disable state storage to MongoDB.
        no_mongodb_statistics (bool): Disable statistics storage to MongoDB.
        clear_mongodb (bool): Clear MongoDB collections.
        playback_speed (int): Playback speed in multiples of real time.
        playback_interval (int): Playback interval in minutes.
        mrt_files (tuple[str, ...]): MRT files to process.

    Returns:
        MRTSimulationResult: The result of the MRT simulation.
    '''
    mrt_simulation_result = MRTSimulationResult(
        count_announce=0,
        count_withdraw=0,
    )

    parser = MrtBgp4MpParser()

    if not no_rabbitmq_direct or rabbitmq_grouped:
        RabbitMQAdapter(
            parser=parser,
            no_direct=no_rabbitmq_direct,
            queue_interval=rabbitmq_grouped,
        )

    if not no_mongodb_log or not no_mongodb_state or not no_mongodb_statistics:
        MongoDBAdapter(
            parser=parser,
            no_mongodb_log=no_mongodb_log,
            no_mongodb_state=no_mongodb_state,
            no_mongodb_statistics=no_mongodb_statistics,
            clear_mongodb=clear_mongodb,
        )

    playback_speed_reference: datetime = None
    playback_interval_stop: datetime = None

    for mrt_file in mrt_files:
        for message in Reader(mrt_file):
            if message.data['type'] != {16: 'BGP4MP'}:
                print('[dark_orange]\[WARN][/] Skipping unsupported MRT type: ', end='')
                print(message.data['type'])
                continue

            current_timestamp: datetime = datetime.fromtimestamp(
                timestamp=list(message.data['timestamp'].keys())[0],
            )

            if playback_speed:
                if playback_speed_reference:
                    time.sleep((current_timestamp - playback_speed_reference).seconds / playback_speed)

                playback_speed_reference = current_timestamp

            if playback_interval:
                if playback_interval_stop:
                    if current_timestamp > playback_interval_stop:
                        input('Enter for next interval...')
                        playback_interval_stop = playback_interval_stop + timedelta(minutes=playback_interval)
                else:
                    playback_interval_stop = current_timestamp + timedelta(minutes=playback_interval)

            updates = parser.parse(
                bgp4mp_message=message,
            )

            if updates:
                for update in updates:
                    if update.change_type == ChangeType.ANNOUNCE:
                        mrt_simulation_result.count_announce += 1
                    elif update.change_type == ChangeType.WITHDRAW:
                        mrt_simulation_result.count_withdraw += 1

    return mrt_simulation_result
