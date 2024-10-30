from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ChangeType(Enum):
    ANNOUNCE = 1,
    WITHDRAW = 2,

class NLRI(BaseModel):
    prefix: str
    length: int

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

class PathAttributes(BaseModel):
    origin: Optional[OriginType] = None
    as_path: Optional[AsPath] = None # !
    next_hop: Optional[list[str]] = None
    multi_exit_disc: Optional[int] = None
    local_pref: Optional[int] = None
    atomic_aggregate: Optional[bool] = None
    aggregator: Optional[Aggregator] = None
    community: Optional[list[list[int]]] = None
    large_community: Optional[list[list[int]]] = None
    extended_community: Optional[list[int]] = None
    orginator_id: Optional[str] = None
    cluster_list: Optional[list[str]] = None

class RouteUpdate(BaseModel):
    timestamp: datetime = datetime.now()
    peer_ip: str
    local_ip: str
    peer_as: int
    local_as: int
    path_attributes: PathAttributes
    change_type: ChangeType = None
    nlri: NLRI = None
