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
from src.models.message_replay import MessageReplayRequest, MessageReplayResult
from src.services.message_replay import message_replay
from fastapi import APIRouter
import json, os

message_replay_router = APIRouter()

@message_replay_router.post('/')
def start_message_replay(message_replay_request: MessageReplayRequest) -> MessageReplayResult:
    '''
    This function starts a message replay.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Args:
        message_replay_request (MessageReplayRequest): The message replay request.

    Returns:
        MessageReplayResult: The message replay result.
    '''
    message_replay_result = message_replay(
        no_rabbitmq_direct=message_replay_request.no_rabbitmq_direct,
        rabbitmq_grouped=message_replay_request.rabbitmq_grouped,
        no_mongodb_log=message_replay_request.no_mongodb_log,
        no_mongodb_state=message_replay_request.no_mongodb_state,
        no_mongodb_statistics=message_replay_request.no_mongodb_statistics,
        clear_mongodb=message_replay_request.clear_mongodb,
        playback_speed=message_replay_request.playback_speed,
        playback_interval=None,
        start_timestamp=None,
        end_timestamp=None,
        start_time=message_replay_request.start_time + ':00',
        end_time=message_replay_request.end_time + ':00',
    )

    return MessageReplayResult(
        count_announce=message_replay_result.count_announce,
        count_withdraw=message_replay_result.count_withdraw,
    )
