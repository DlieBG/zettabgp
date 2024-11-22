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
from src.parsers.route_update import RouteUpdateParser
from src.models.route_update import RouteUpdate
from datetime import timedelta, datetime
import pika, json, os

class RabbitMQAdapter:
    '''
    This class is responsible for receiving the parsed messages and forwarding them to the RabbitMQ message broker.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    def __init__(self, parser: RouteUpdateParser, no_direct: bool, queue_interval: int):
        '''
        Initializes the RabbitMQAdapter.

        Author:
            Benedikt Schwering <bes9584@thi.de>

        Args:
            parser (RouteUpdateParser): The parser to receive the parsed messages from.
            no_direct (bool): Whether to disable the direct route updates.
            queue_interval (int): The interval in minutes to group the route updates.
        '''
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv('RABBIT_MQ_HOST', 'localhost'),
            )
        )

        # Creates a channel for the connection and declares the zettabgp exchange
        channel = connection.channel()
        channel.exchange_declare(
            exchange='zettabgp',
            exchange_type='direct',
        )

        # Declares the test_bgp_updates queue and binds it to the zettabgp exchange
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
            queue_name='test_direct_route_updates',
            routing_key='direct',
        )
        _declare_test_queue(
            queue_name='test_grouped_route_updates',
            routing_key='grouped',
        )

        if not no_direct:
            @parser.on_update
            def direct(message: RouteUpdate):
                channel.basic_publish(
                    exchange='zettabgp',
                    body=message.model_dump_json(),
                    routing_key='direct',
                )

        if queue_interval:
            queue_interval_stop: datetime = None
            queue_interval_messages: list[RouteUpdate] = []
        
            @parser.on_update
            def grouped(message: RouteUpdate):
                nonlocal queue_interval_stop

                if queue_interval_stop:
                    if message.timestamp >= queue_interval_stop:
                        channel.basic_publish(
                            exchange='zettabgp',
                            body=json.dumps([
                                message.model_dump(
                                    mode='json',
                                ) 
                                    for message in queue_interval_messages
                            ]),
                            routing_key='grouped',
                        )

                        queue_interval_stop = queue_interval_stop + timedelta(minutes=queue_interval)
                        queue_interval_messages.clear()
                else:
                    # -1 seconds to avoid unpublished last interval when the next message is exactly at the stop time
                    # this occurs when simulating with mrt-simulation and same -o value
                    queue_interval_stop = message.timestamp + timedelta(minutes=queue_interval, seconds=-1)

                queue_interval_messages.append(message)
