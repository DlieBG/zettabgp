from src.parsers.mrt_bgp4mp import MrtBgp4MpParser
from src.adapters.rabbitmq import RabbitMQAdapter
from src.adapters.mongodb import MongoDBAdapter
from src.parsers.exabgp import ExaBGPParser
from datetime import timedelta, datetime
from mrtparse import Reader
import click, time, sys
from rich import print

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
def exabgp(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool):
    parser = ExaBGPParser()

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
        )

    while True:
        for line in sys.stdin:
            parser.parse(
                line=line,
            )

        time.sleep(1)

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
    'mrt_file',
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
)
def mrt_simulation(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, playback_speed: int, playback_interval: int, mrt_file: str):
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
        )

    playback_speed_reference: datetime = None
    playback_interval_stop: datetime = None

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

        parser.parse(
            bgp4mp_message=message,
        )
