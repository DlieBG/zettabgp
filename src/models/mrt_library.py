from pydantic import BaseModel
from typing import Optional

class MRTScenarioRequest(BaseModel):
    id: str

class MRTScenarioResult(BaseModel):
    count_announce: int
    count_withdraw: int

class MRTScenario(BaseModel):
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
    scenarios: list[MRTScenario]
