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
from src.adapters.rabbitmq import RabbitMQAdapter
from src.adapters.mongodb import MongoDBAdapter
from src.parsers.rib import RibParser
from mrtparse import Reader
from rich import print

def rib_load(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool, rib_file: str):
    '''
    RIB Load service for retrieving BGP routes from RIB files and loading them.

    Author:
        Sebastian Forstner <sef9869@thi.de>

    Args:
        no_rabbitmq_direct (bool): Disable direct RabbitMQ direct queue..
        rabbitmq_grouped (int): Queue group interval in minutes.
        no_mongodb_log (bool): Disable logging to MongoDB.
        no_mongodb_state (bool): Disable state storage to MongoDB.
        no_mongodb_statistics (bool): Disable statistics storage to MongoDB.
        clear_mongodb (bool): Clear MongoDB collections.
        rib_file (str): RIB file to process.
    '''
    parser = RibParser()

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

    for message in Reader(rib_file):
        if message.data['type'] != {13: 'TABLE_DUMP_V2'}:
            print('[dark_orange]\[WARN][/] Skipping unsupported MRT type: ', end='')
            print(message.data['type'])
            continue

        parser.parse(
            statement=message.data,
        )
