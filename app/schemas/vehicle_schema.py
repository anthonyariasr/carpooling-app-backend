from pydantic import BaseModel
from typing import Optional

from app.schemas.brand_schema import BrandResponse
from app.schemas.vehicle_type_schema import VehicleTypeResponse

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
    vehicle_type: VehicleTypeResponse
    brand: BrandResponse

    class Config:
        from_attributes = True

class VehicleBasicInfo(BaseModel):
    id: int
    license_plate: str
    brand: str
