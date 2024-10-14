from pydantic import BaseModel
from typing import Optional

from app.schemas.stop_schema import StopBasicInfo

class TripPassengerCreate(BaseModel):
    trip_id: int
    user_id: int
    pick_up_stop_name: str
    pick_up_stop_description: Optional[str] = None
    pick_up_stop_latitude: Optional[str] = None
    pick_up_stop_longitude: Optional[str] = None

class TripPassengerResponse(BaseModel):
    trip_id: int
    user_id: int
    pickup_stop: StopBasicInfo

    class Config:
        from_attributes = True
