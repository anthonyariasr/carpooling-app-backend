from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import *
from app.schemas import *

trip_status_router = APIRouter()

@trip_status_router.get("", response_model=List[TripStatusResponse])
def get_all_trip_statuses(db: Session = Depends(get_db)):
    trip_statuses = db.query(TripStatus).all()
    return trip_statuses