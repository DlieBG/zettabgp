from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class OriginType(Enum):
    IGP = 1
    EGP = 2
    INCOMPLETE = 3

class AsPathType(Enum):
    AS_SET = 1
    AS_SEQUENCE = 2
    AS_CONFED_SET = 3
    AS_CONFED_SEQUENCE = 4

class AsPath(BaseModel):
    type: AsPathType
    value: list[int]

class Aggregator(BaseModel):
    router_id: str
    router_as: int

class Network(BaseModel):
    prefix: str
    mask: int

class PathAttributes(BaseModel):
    origin: Optional[OriginType] = None
    as_path: Optional[AsPath] = None
    next_hop: Optional[list[str]] = None
    multi_exit_disc: int = 0
    local_pref: int = 100
    atomic_aggregate: bool = False
    aggregator: Optional[Aggregator] = None
    community: Optional[list[list[int]]] = None
    large_community: Optional[list[list[int]]] = None
    extended_community: Optional[list[int]] = None
    orginator_id: Optional[str] = None
    cluster_list: Optional[list[str]] = None
    mp_reach_nlri: list[Network] = []
    mp_unreach_nlri: list[Network] = []

class BGPUpdateMessage(BaseModel):
    timestamp: datetime = datetime.now()
    peer_ip: str = None
    local_ip: str = None
    peer_as: int = None
    local_as: int = None
    withdrawn_routes: list[Network] = []
    path_attributes: Optional[PathAttributes] = None
