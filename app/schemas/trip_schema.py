from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime, time

from app.schemas.institution_schema import InstitutionBasicInfo
from app.schemas.stop_schema import StopBasicInfo
from app.schemas.trip_status_schema import TripStatusResponse
from app.schemas.user_schema import UserBasicInfo
from app.schemas.vehicle_schema import VehicleBasicInfo
class TripCreate(BaseModel):
    passenger_limit: int
    fare_per_person: int
    route_url: str
    departure_datetime: datetime
    driver_id: int
    starting_point_id: int
    finishing_point_id: int
    trip_status_id: int
    vehicle_id: int

class TripResponse(BaseModel):
    id: int
    passenger_limit: int
    fare_per_person: float
    route_url: Optional[str]
    departure_date: date
    departure_time: time
    driver: UserBasicInfo
    starting_point: StopBasicInfo
    finishing_point: StopBasicInfo
    trip_status: TripStatusResponse
    vehicle: VehicleBasicInfo
    institution: InstitutionBasicInfo

    class Config:
        from_attributes = True

class TripBasicInfo(BaseModel):
    starting_point: StopBasicInfo
    finishing_point: StopBasicInfo
    departure_date: date
    driver: UserBasicInfo