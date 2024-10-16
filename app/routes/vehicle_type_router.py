from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import *
from app.schemas import *

vehicle_type_router = APIRouter()

@vehicle_type_router.get("", response_model=List[VehicleTypeResponse])
def get_all_vehicle_types(db: Session = Depends(get_db)):
    vehicle_types = db.query(VehicleType).all()
    return vehicle_types