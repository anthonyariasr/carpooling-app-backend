from pydantic import BaseModel
from typing import Optional

class TripPassengerCreate(BaseModel):
    trip_id: int
    user_id: int
    pickup_stop_id: Optional[int] #optional?

class TripPassengerResponse(BaseModel):
    trip_id: int
    user_id: int
    pickup_stop_id: Optional[int]

    class Config:
        orm_mode = True
