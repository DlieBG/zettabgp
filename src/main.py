from src.adapters.rabbitmq import RabbitMQAdapter
from src.parsers.exabgp import ExaBGPParser
import click, time, sys

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

# @cli.command(
#     name='mrt-simulation',
#     help='Process MRT files.',
# )
# def mrt_simulation():
#     pass