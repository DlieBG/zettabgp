from src.adapters.rabbitmq import RabbitMQAdapter
from src.adapters.mongodb import MongoDBAdapter
from src.parsers.exabgp import ExaBGPParser
import time, sys

def exabgp(no_rabbitmq_direct: bool, rabbitmq_grouped: int, no_mongodb_log: bool, no_mongodb_state: bool, no_mongodb_statistics: bool, clear_mongodb: bool):
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
            clear_mongodb=clear_mongodb,
        )

    while True:
        for line in sys.stdin:
            parser.parse(
                line=line,
            )

        time.sleep(1)
