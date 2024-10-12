
from typing import List, Optional
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from app.database import *
from app.schemas import *

trip_router = APIRouter()

def prepare_trip(trip: Trip):
    return {
        "id": trip.id,
        "passenger_limit": trip.passenger_limit,
        "fare_per_person": trip.fare_per_person,
        "route_url": trip.route_url,
        "departure_date": trip.departure_datetime.date(),
        "departure_time": trip.departure_datetime.time(),
        "driver": {
            "id": trip.driver_id,
            "name": f"{trip.driver.first_name} {trip.driver.first_surname}",
            "rating": trip.driver.rating
        },
        "starting_point": {
            "id": trip.starting_point_id,
            "name": trip.starting_point.name
        },
        "finishing_point": {
            "id": trip.finishing_point_id,
            "name": trip.finishing_point.name
        },
        "trip_status": {
            "id": trip.trip_status_id,
            "name": trip.trip_status.name
        },
        "vehicle": {
            "id": trip.vehicle_id,
            "license_plate": trip.vehicle.license_plate,
            "brand": trip.vehicle.brand.name
        },
        "institution": {
            "id": trip.driver.institution.id,
            "name": trip.driver.institution.name,
            "acronym": trip.driver.institution.acronym
        }
    }

@trip_router.get("/", response_model=List[TripResponse], status_code=status.HTTP_200_OK)
def get_trips(
    trip_status_id: Optional[int] = None,
    starting_point: Optional[str] = None,
    finishing_point: Optional[str] = None,
    departure_date: Optional[date] = None, 
    driver_id: Optional[int] = None,
    passenger_id: Optional[int] = None,
    db: Session = Depends(get_db) 
):
    trips = db.query(Trip)
    
    # Crear alias para evitar ambigüedad
    starting_point_alias = aliased(Stop)
    finishing_point_alias = aliased(Stop)

    if starting_point is not None:
        trips = trips.join(starting_point_alias, Trip.starting_point_id == starting_point_alias.id).filter(starting_point_alias.name == starting_point)
    if finishing_point is not None:
        trips = trips.join(finishing_point_alias, Trip.finishing_point_id == finishing_point_alias.id).filter(finishing_point_alias.name == finishing_point)
    if finishing_point is not None:
        trips = trips.join(Stop, Trip.finishing_point_id == Stop.id).filter(Stop.name == finishing_point)
    if trip_status_id is not None:
        trips = trips.filter(Trip.trip_status_id == trip_status_id)
    if departure_date is not None:
        trips = trips.filter(func.date(Trip.departure_datetime) == departure_date)
    if driver_id is not None:
        trips = trips.filter(Trip.driver_id == driver_id)
    if passenger_id is not None:
        trips = trips.join(trip_passengers).filter(trip_passengers.c.user_id == passenger_id)
    if trips.count() == 0:
        raise HTTPException(status_code=404, detail="No trip found")

    return [prepare_trip(trip) for trip in trips.all()]

@trip_router.get("/{trip_id}", response_model=TripResponse, status_code=status.HTTP_200_OK)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return prepare_trip(trip)
