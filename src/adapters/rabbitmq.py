from src.parsers.route_update import RouteUpdateParser
from src.models.route_update import RouteUpdate
import pika, os

class RabbitMQAdapter:
    def __init__(self, parser: RouteUpdateParser):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv('RABBIT_MQ_HOST', 'localhost'),
            )
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange='zettabgp',
            exchange_type='fanout',
        )

        # Test queue
        def _declare_test_queue(queue_name: str):
            channel.queue_declare(
                queue=queue_name,
            )
            channel.queue_bind(
                exchange='zettabgp',
                queue=queue_name,
            )

        _declare_test_queue(
            queue_name='test_bgp_updates',
        )

        @parser.on_update
        def on_update(message: RouteUpdate):
            channel.basic_publish(
                exchange='zettabgp',
                body=message.model_dump_json(),
                routing_key='',
            )
