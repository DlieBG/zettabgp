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
from src.adapters.mongodb import MongoDBAdapter, MongoDBLogLoader
from src.adapters.rabbitmq import RabbitMQAdapter
from src.parsers.reverse import ReverseParser
from datetime import timedelta, datetime
from collections import OrderedDict
import time

def message_replay(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool, playback_speed: int, playback_interval: int, start_timestamp: float, end_timestamp: float, start_time: str, end_time: str):
    '''
    Message replay service for replaying BGP messages from Database log.

    Author:
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
        start_timestamp (float): Starttime of replay as timestamp.
        end_timestamp (float): Endtime of replay as timestamp.
        start_time (str): Starttime of replay as time; in format (T is a set character): YYYY-MM-DDThh:mm:ss.
        end_time (str): Endtime of replay as time; in format (T is a set character): YYYY-MM-DDThh:mm:ss.
    '''
    parser = ReverseParser()

    if not no_rabbitmq_direct or rabbitmq_grouped:
        RabbitMQAdapter(
            parser=parser,
            no_direct=no_rabbitmq_direct,
            queue_interval=rabbitmq_grouped,
        )
    
    playback_speed_reference: datetime = None
    playback_interval_stop: datetime = None

    # Check if start and end are given and in which format; no time given results in replaying whole db
    if start_timestamp and end_timestamp:
        start_time = datetime.fromtimestamp(start_timestamp)
        end_time = datetime.fromtimestamp(end_timestamp)
        new_messages = MongoDBLogLoader.load_messages(timestamp_start = start_time, timestamp_end = end_time)
    elif start_time and end_time: 
        time_start = datetime.fromisoformat(start_time)
        time_end = datetime.fromisoformat(end_time)
        new_messages = MongoDBLogLoader.load_messages(timestamp_start = time_start, timestamp_end = time_end)
    else:
        new_messages = MongoDBLogLoader.load_messages(timestamp_start = None, timestamp_end = None)

    # Copy messages in local list to avoid deleting them if -c is set; new_messages is corsor pointing to db
    all_messages: list[OrderedDict] = []
    for message in new_messages:
        all_messages.append(message)

    # Init for MongoDBAdapter to avouid deleting messages before loading
    if not no_mongodb_log or not no_mongodb_state or not no_mongodb_statistics:
        MongoDBAdapter(
            parser=parser,
            no_mongodb_log=no_mongodb_log,
            no_mongodb_state=no_mongodb_state,
            no_mongodb_statistics=no_mongodb_statistics,
            clear_mongodb=clear_mongodb,
        )

    for message in all_messages:
        current_timestamp: datetime = message['timestamp']

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

        parser.parse(message)
