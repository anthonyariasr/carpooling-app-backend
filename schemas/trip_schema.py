from pydantic import BaseModel
from typing import Optional

class TripCreate(BaseModel):
    passenger_limit: int
    fare_per_person: int
    route_url: str
    departure_datetime: str
    driver_id: int
    starting_point_id: int
    finishing_point_id: int
    trip_status_id: int
    vehicle_id: int

class TripResponse(BaseModel):
    id: int
    passenger_limit: int
    fare_per_person: int
    route_url: str
    departure_datetime: str
    driver_id: int
    starting_point_id: int
    finishing_point_id: int
    trip_status_id: int
    vehicle_id: int

    class Config:
        orm_mode = True
