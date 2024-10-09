from pydantic import BaseModel
from typing import Optional

class StopCreate(BaseModel):
    latitude: str
    longitude: str
    name: str
    description: Optional[str]

class StopResponse(BaseModel):
    id: int
    latitude: str
    longitude: str
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
