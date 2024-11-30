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
from pydantic import BaseModel
from typing import Optional

class MessageReplayRequest(BaseModel):
    '''
    This class represents a request to replay messages.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    no_rabbitmq_direct: bool
    rabbitmq_grouped: Optional[int]
    no_mongodb_log: bool
    no_mongodb_state: bool
    no_mongodb_statistics: bool
    clear_mongodb: bool
    playback_speed: Optional[int]
    start_time: str
    end_time: str

class MessageReplayResult(BaseModel):
    '''
    This class represents the result of replay messages.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    count_withdraw: int
    count_announce: int
