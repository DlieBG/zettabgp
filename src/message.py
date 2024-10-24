from pydantic import BaseModel
from datetime import datetime
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
    origin: OriginType = None
    as_path: AsPath = None
    next_hop: list[str] = []
    multi_exit_disc: int = 0
    local_pref: int = 100
    atomic_aggregate: bool = False
    aggregator: Aggregator = None
    community: list[list[int]] = [] # including large community
    orginator_id: str = None
    cluster_list: list[str] = []
    mp_reach_nlri: list[Network] = []
    mp_unreach_nlri: list[Network] = []
    extended_community: list[int] = []

class BGPUpdateMessage(BaseModel):
    timestamp: datetime
    peer_ip: str
    local_ip: str
    peer_as: int
    local_as: int
    withdrawn_routes: list[Network]
    path_attributes: list[PathAttributes]
