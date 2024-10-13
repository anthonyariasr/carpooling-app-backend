from pydantic import BaseModel
from typing import Optional

from app.schemas.stop_schema import StopBasicInfo

class TripPassengerCreate(BaseModel):
    trip_id: int
    user_id: int
    pickup_stop_id: Optional[int] #optional?

class TripPassengerResponse(BaseModel):
    trip_id: int
    user_id: int
    pickup_stop: StopBasicInfo

    class Config:
        from_attributes = True
