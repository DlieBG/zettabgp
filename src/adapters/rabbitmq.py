from parser import BGPParser
from message import Message
import pika

class RabbitMQAdapter:
    '''This class is responsible for receiving the parsed messages and forwarding them to RabbitMQ.'''
    def __init__(self, parser: BGPParser):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
            )
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange='zettabgp',
            exchange_type='topic',
        )

        # Test queues
        def _declare_test_queue(queue_name: str, routing_key: str):
            channel.queue_declare(
                queue=queue_name,
            )
            channel.queue_bind(
                exchange='zettabgp',
                queue=queue_name,
                routing_key=routing_key,
            )

        _declare_test_queue(
            queue_name='test_bgp_updates',
            routing_key='*',
        )
        _declare_test_queue(
            queue_name='test_bgp_announces',
            routing_key='announce',
        )
        _declare_test_queue(
            queue_name='test_bgp_withdraws',
            routing_key='withdraw',
        )

        @parser.on_announce
        def on_announce(message: Message):
            channel.basic_publish(
                exchange='zettabgp',
                routing_key='announce',
                body=message.model_dump_json(),
            )

            # print('[rabbitmq] announce ok')

        @parser.on_withdraw
        def on_withdraw(message: Message):
            channel.basic_publish(
                exchange='zettabgp',
                routing_key='withdraw',
                body=message.model_dump_json(),
            )

            # print('[rabbitmq] withdraw ok')
