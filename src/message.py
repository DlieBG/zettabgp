from pydantic import BaseModel
from typing import Optional

class _Address(BaseModel):
    local: str
    peer: str

class _Asn(BaseModel):
    local: int
    peer: int

class _Update(BaseModel):
    attribute: Optional[dict] = None
    announce: Optional[dict] = None
    withdraw: Optional[dict] = None

class _Message(BaseModel):
    update: Optional[_Update] = None

class Message(BaseModel):
    address: _Address
    asn: _Asn
    direction: str
    message: _Message
