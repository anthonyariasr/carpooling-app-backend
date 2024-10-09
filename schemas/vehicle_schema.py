from pydantic import BaseModel
from typing import Optional

class VehicleCreate(BaseModel):
    license_plate: str
    year: str
    max_capacity: int
    description: Optional[str]
    owner_id: int
    vehicle_type_id: int
    brand_id: int

class VehicleResponse(BaseModel):
    id: int
    license_plate: str
    year: str
    max_capacity: int
    description: Optional[str]
    owner_id: int
    vehicle_type_id: int
    brand_id: int

    class Config:
        orm_mode = True
