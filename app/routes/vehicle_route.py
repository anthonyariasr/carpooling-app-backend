# app/routes/vehicle_route.py

from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleResponse

vehicle_router = APIRouter()

def prepare_vehicle(vehicle: Vehicle):
    return {
        "id": vehicle.id,
        "license_plate": vehicle.license_plate,
        "year": vehicle.year,
        "max_capacity": vehicle.max_capacity,
        "description": vehicle.description,
        "owner_id": vehicle.owner_id,
        "vehicle_type": {
            "id": vehicle.vehicle_type.id,
            "name": vehicle.vehicle_type.name
        },
        "brand": {
            "id": vehicle.brand.id,
            "name": vehicle.brand.name
        }
    }

@vehicle_router.get("/", response_model=List[VehicleResponse], status_code=status.HTTP_200_OK)
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).all()
    if not vehicles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No vehicles found")
    return [prepare_vehicle(vehicle) for vehicle in vehicles]

@vehicle_router.get("/{vehicle_id}", response_model=VehicleResponse, status_code=status.HTTP_200_OK)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return prepare_vehicle(vehicle)

@vehicle_router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    new_vehicle = Vehicle(
        license_plate=vehicle.license_plate,
        year=vehicle.year,
        max_capacity=vehicle.max_capacity,
        description=vehicle.description,
        owner_id=vehicle.owner_id,
        vehicle_type_id=vehicle.vehicle_type_id,
        brand_id=vehicle.brand_id
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return prepare_vehicle(new_vehicle)

# Endpoint para actualizar un vehículo
from pydantic import BaseModel

class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    brand_id: Optional[int] = None
    vehicle_type_id: Optional[int] = None
    max_capacity: Optional[int] = None

@vehicle_router.put("/{vehicle_id}", response_model=VehicleResponse, status_code=status.HTTP_200_OK)
def update_vehicle(vehicle_id: int, vehicle_update: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle_db = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    
    update_data = vehicle_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vehicle_db, key, value)
    
    db.commit()
    db.refresh(vehicle_db)
    return prepare_vehicle(vehicle_db)

# Endpoint para eliminar un vehículo
@vehicle_router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return
