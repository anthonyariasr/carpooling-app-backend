from pydantic import BaseModel
from typing import Optional

class TripStatusCreate(BaseModel):
    name: str

class TripStatusResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
