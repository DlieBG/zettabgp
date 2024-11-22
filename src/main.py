import src.services.mrt_simulation as mrt_simulation_service
import src.services.exabgp as exabgp_service
from src.webapp import start_webapp
import click

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
def mrt_simulation(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool, playback_speed: int, playback_interval: int, mrt_files: tuple[str]):
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
    start_webapp(
        reload=reload,
    )
