from src.parsers.mrt_bgp4mp import MrtBgp4MpParser
from src.adapters.rabbitmq import RabbitMQAdapter
from src.parsers.exabgp import ExaBGPParser
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
    '--no-rabbitmq',
    '-r',
    is_flag=True,
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
def exabgp(no_rabbitmq: bool, no_mongodb_log: bool, no_mongodb_state: bool):
    parser = ExaBGPParser()

    if not no_rabbitmq:
        RabbitMQAdapter(
            parser=parser,
        )

    if not no_mongodb_log:
        pass

    if not no_mongodb_state:
        pass

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
    '--no-rabbitmq',
    '-r',
    is_flag=True,
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
@click.argument(
    'mrt_file',
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
)
def mrt_simulation(no_rabbitmq: bool, no_mongodb_log: bool, no_mongodb_state: bool, mrt_file: str):
    parser = MrtBgp4MpParser()

    if not no_rabbitmq:
        RabbitMQAdapter(
            parser=parser,
        )

    if not no_mongodb_log:
        pass

    if not no_mongodb_state:
        pass

    for entry in Reader(mrt_file):
        if entry.data['type'] != {16: 'BGP4MP'}:
            print('[dark_orange]\[WARN][/] Skipping unknown MRT type: ', end='')
            print(entry.data['type'])
            continue

        parser.parse(
            mrt=entry,
        )
