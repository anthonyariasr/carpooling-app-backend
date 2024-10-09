from pydantic import BaseModel
from typing import Optional

class TripStatusCreate(BaseModel):
    name: str
    description: Optional[str]

class TripStatusResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
