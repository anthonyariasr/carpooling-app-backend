from pydantic import BaseModel
from typing import Optional

class StopCreate(BaseModel):
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    name: str
    description: Optional[str] = None

class StopResponse(BaseModel):
    id: int
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class StopBasicInfo(BaseModel):
    id: int
    name: str