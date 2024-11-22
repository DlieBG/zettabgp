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

class MRTScenarioRequest(BaseModel):
    '''
    This class represents a request to run an MRT scenario.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    id: str

class MRTScenarioResult(BaseModel):
    '''
    This class represents the result of an MRT scenario.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    count_announce: int
    count_withdraw: int

class MRTScenario(BaseModel):
    '''
    This class represents an MRT scenario.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    id: str
    path: str
    name: str
    description: str
    no_rabbitmq_direct: bool
    rabbitmq_grouped: Optional[int]
    no_mongodb_log: bool
    no_mongodb_state: bool
    no_mongodb_statistics: bool
    clear_mongodb: bool
    playback_speed: Optional[int]
    mrt_files: list[str]

class MRTLibrary(BaseModel):
    '''
    This class represents an MRT library.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    scenarios: list[MRTScenario]
