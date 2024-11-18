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
from src.adapters.mongodb import MongoDBAdapter, DB_logoutput
import src.services.mrt_simulation as mrt_simulation_service
from src.adapters.rabbitmq import RabbitMQAdapter
from src.parsers.dbreverse import ReverseParser
import src.services.exabgp as exabgp_service
from datetime import timedelta, datetime
from src.parsers.rib import RibParser
from collections import OrderedDict
from src.webapp import start_webapp
from mrtparse import Reader
from rich import print
import click, time

@click.group()
def cli():
    pass

@cli.command(
    name='exabgp',
    help='Process ExaBGP messages.',
)
@click.option(
    '--no-rabbitmq-direct',
    '-d',
    is_flag=True,
)
@click.option(
    '--rabbitmq-grouped',
    '-g',
    type=int,
    default=None,
    show_default='5',
    is_flag=False,
    flag_value=5,
    help='Queue group interval in minutes.',
)
@click.option(
    '--no-mongodb-log',
    '-l',
    is_flag=True,
)
@click.option(
    '--no-mongodb-state',
    '-s',
    is_flag=True,
)
@click.option(
    '--no-mongodb-statistics',
    '-t',
    is_flag=True,
)
@click.option(
    '--clear-mongodb',
    '-c',
    is_flag=True,
)
def exabgp(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool):
    '''
    ExaBGP command for retrieving BGP messages from ExaBGP via stdin and processing them.

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
    '''
    exabgp_service.exabgp(
        no_rabbitmq_direct=no_rabbitmq_direct,
        rabbitmq_grouped=rabbitmq_grouped,
        no_mongodb_log=no_mongodb_log,
        no_mongodb_state=no_mongodb_state,
        no_mongodb_statistics=no_mongodb_statistics,
        clear_mongodb=clear_mongodb,
    )

@cli.command(
    name='mrt-simulation',
    help='Process BGP4MP MRT files.',
)
@click.option(
    '--no-rabbitmq-direct',
    '-d',
    is_flag=True,
)
@click.option(
    '--rabbitmq-grouped',
    '-g',
    type=int,
    default=None,
    show_default='5',
    is_flag=False,
    flag_value=5,
    help='Queue group interval in minutes.',
)
@click.option(
    '--no-mongodb-log',
    '-l',
    is_flag=True,
)
@click.option(
    '--no-mongodb-state',
    '-s',
    is_flag=True,
)
@click.option(
    '--no-mongodb-statistics',
    '-t',
    is_flag=True,
)
@click.option(
    '--clear-mongodb',
    '-c',
    is_flag=True,
)
@click.option(
    '--playback-speed',
    '-p',
    type=int,
    default=None,
    show_default='1',
    is_flag=False,
    flag_value=1,
    help='Playback speed in multiples of real time.',
)
@click.option(
    '--playback-interval',
    '-o',
    type=int,
    default=None,
    show_default='5',
    is_flag=False,
    flag_value=5,
    help='Playback interval in minutes.',
)
@click.argument(
    'mrt_files',
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=True,
    nargs=-1,
)
def mrt_simulation(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool, playback_speed: int, playback_interval: int, mrt_files: tuple[str, ...]):
    '''
    MRT Simulation command for retrieving BGP messages from MRT files and processing them.

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
    '''
    mrt_simulation_service.mrt_simulation(
        no_rabbitmq_direct=no_rabbitmq_direct,
        rabbitmq_grouped=rabbitmq_grouped,
        no_mongodb_log=no_mongodb_log,
        no_mongodb_state=no_mongodb_state,
        no_mongodb_statistics=no_mongodb_statistics,
        clear_mongodb=clear_mongodb,
        playback_speed=playback_speed,
        playback_interval=playback_interval,
        mrt_files=mrt_files,
    )

@cli.command(
    name='webapp',
    help='Open the admin webapp.',
)
@click.option(
    '--reload',
    '-r',
    is_flag=True,
)
def webapp(reload: bool):
    '''
    WebApp command for launching the admin WebApp.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Args:
        reload (bool): Reload the WebApp on changes.
    '''
    start_webapp(
        reload=reload,
    )

@cli.command(
    name='rib-load',
    help='Load a rib-file in ZettaBGP.',
)
@click.option(
    '--no-rabbitmq-direct',
    '-d',
    is_flag=True,
)
@click.option(
    '--rabbitmq-grouped',
    '-g',
    type=int,
    default=None,
    show_default='5',
    is_flag=False,
    flag_value=5,
    help='Queue group interval in minutes.',
)
@click.option(
    '--no-mongodb-log',
    '-l',
    is_flag=True,
)
@click.option(
    '--no-mongodb-state',
    '-s',
    is_flag=True,
)
@click.option(
    '--no-mongodb-statistics',
    '-t',
    is_flag=True,
)
@click.option(
    '--clear-mongodb',
    '-c',
    is_flag=True,
)
@click.argument(
    'rib_file',
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
)
def rib_load(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool, rib_file: str):
    '''
    RIB Load command for retrieving BGP routes from RIB files and loading them.

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

@cli.command(
    name='message-replay',
    help='Replay messages from database.',
)
@click.option(
    '--no-rabbitmq-direct',
    '-d',
    is_flag=True,
)
@click.option(
    '--rabbitmq-grouped',
    '-g',
    type=int,
    default=None,
    show_default='5',
    is_flag=False,
    flag_value=5,
    help='Queue group interval in minutes.',
)
@click.option(
    '--no-mongodb-log',
    '-l',
    is_flag=True,
)
@click.option(
    '--no-mongodb-state',
    '-s',
    is_flag=True,
)
@click.option(
    '--no-mongodb-statistics',
    '-t',
    is_flag=True,
)
@click.option(
    '--clear-mongodb',
    '-c',
    is_flag=True,
)
@click.option(
    '--playback-speed',
    '-p',
    type=int,
    default=None,
    show_default='1',
    is_flag=False,
    flag_value=1,
    help='Playback speed in multiples of real time.',
)
@click.option(
    '--playback-interval',
    '-o',
    type=int,
    default=None,
    show_default='5',
    is_flag=False,
    flag_value=5,
    help='Playback interval in minutes.',
)
@click.option(
    '--start-timestamp',
    '-b',
    type=float,
    default=None,
    help='Starttime of replay as timestamp',
)
@click.option(
    '--end-timestamp',
    '-e',
    type=float,
    default=None,
    help='Endtime of replay as timestamp',
)
@click.option(
    '--start-time',
    '-r',
    type=str,
    help='Starttime of replay as time; in format (T is a set character): YYYY-MM-DDThh:mm:ss',
)
@click.option(
    '--end-time',
    '-f',
    type=str,
    help='Endtime of replay as time; in format (T is a set character): YYYY-MM-DDThh:mm:ss',
)
def message_replay(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool, playback_speed: int, playback_interval: int, start_timestamp: float, end_timestamp: float, start_time: str, end_time: str):
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
        new_messages = DB_logoutput.load_messages(timestamp_start = start_time, timestamp_end = end_time)
    elif start_time and end_time: 
        time_start = datetime.fromisoformat(start_time)
        time_end = datetime.fromisoformat(end_time)
        new_messages = DB_logoutput.load_messages(timestamp_start = time_start, timestamp_end = time_end)
    else:
        new_messages = DB_logoutput.load_messages(timestamp_start = None, timestamp_end = None)

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
