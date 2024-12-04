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
from datetime import datetime
from typing import Optional
from enum import Enum

class ChangeType(Enum):
    '''
    This class represents the change type of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    ANNOUNCE = 1,
    WITHDRAW = 2,

class NLRI(BaseModel):
    '''
    This class represents the network layer reachability information of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    prefix: str
    length: int

class OriginType(Enum):
    '''
    This class represents the origin type of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    IGP = 1
    EGP = 2
    INCOMPLETE = 3

class AsPathType(Enum):
    '''
    This class represents the AS path type of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    AS_SET = 1
    AS_SEQUENCE = 2
    AS_CONFED_SET = 3
    AS_CONFED_SEQUENCE = 4

class AsPath(BaseModel):
    '''
    This class represents the AS path of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    type: AsPathType
    value: list[int]

class Aggregator(BaseModel):
    '''
    This class represents the aggregator of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    router_id: str
    router_as: int

class PathAttributes(BaseModel):
    '''
    This class represents the path attributes of a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    origin: Optional[OriginType] = None
    as_path: Optional[list[AsPath]] = None
    next_hop: Optional[list[str]] = None
    multi_exit_disc: Optional[int] = None
    local_pref: Optional[int] = None
    atomic_aggregate: Optional[bool] = None
    aggregator: Optional[Aggregator] = None
    community: Optional[list[list[int]]] = None
    large_community: Optional[list[list[int]]] = None
    extended_community: Optional[list[str]] = None
    orginator_id: Optional[str] = None
    cluster_list: Optional[list[str]] = None

class RouteUpdate(BaseModel):
    '''
    This class represents a route update.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    timestamp: datetime = datetime.now()
    peer_ip: str
    local_ip: str
    peer_as: int
    local_as: int
    path_attributes: PathAttributes
    change_type: ChangeType = None
    nlri: NLRI = None
