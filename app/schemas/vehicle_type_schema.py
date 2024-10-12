from pydantic import BaseModel

class VehicleTypeCreate(BaseModel):
    name: str

class VehicleTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
