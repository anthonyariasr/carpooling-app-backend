
from typing import List, Optional
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, HTTPException, status
from sqlalchemy import func, insert, or_
from sqlalchemy.orm import Session, aliased
from app.database import *
from app.schemas import *

trip_router = APIRouter()

def prepare_trip(trip: Trip):
    return {
        "id": trip.id,
        "passenger_limit": trip.passenger_limit,
        "passenger_count": len(trip.passengers),
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

def prepare_user(user: User):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "first_surname": user.first_surname,
        "second_surname": user.second_surname,
        "identification": user.identification,
        "institutional_email": user.institutional_email,
        "phone_number": user.phone_number,
        "birth_date": user.birth_date,
        "gender": {
            "id": user.gender.id,
            "name": user.gender.name
        },
        "user_type": {
            "id": user.user_type.id,
            "name": user.user_type.name
        },
        "institution": {
            "id": user.institution.id,
            "name": user.institution.name,
            "acronym": user.institution.acronym
        },
        "date_registered": user.date_registered,
        "rating": user.rating,
        "total_ratings": user.total_ratings
    }

@trip_router.get("", response_model=List[TripResponse], status_code=status.HTTP_200_OK)
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

@trip_router.get("/user/{user_id}", response_model=TripResponse, status_code=status.HTTP_200_OK)
def get_trip_of_user(user_id: int, db: Session = Depends(get_db)):
    trip = (
        db.query(Trip)
        .join(trip_passengers, trip_passengers.c.trip_id == Trip.id)
        .filter(
            trip_passengers.c.user_id == user_id,
            or_(Trip.trip_status.has(name="Pending"), Trip.trip_status.has(name="Active"))
        )
        .first()
    )
    
    if trip is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trip found for this user")

    return prepare_trip(trip)

@trip_router.get("/{trip_id}/passengers", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_passengers_of_trip(trip_id: int, db: Session = Depends(get_db)):
    passengers = (
        db.query(User)
        .join(trip_passengers, trip_passengers.c.user_id == User.id)
        .filter(trip_passengers.c.trip_id == trip_id)
    )

    if passengers.count() == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No passengers found for this trip")
    
    return [prepare_user(user) for user in passengers.all()]

@trip_router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    starting_point = Stop(name=trip.starting_point_name, latitude=trip.starting_point_latitude, longitude=trip.starting_point_longitude, description=trip.starting_point_description)
    finishing_point = Stop(name=trip.finishing_point_name, latitude=trip.finishing_point_latitude, longitude=trip.finishing_point_longitude, description=trip.finishing_point_description)
    db.add(starting_point)
    db.add(finishing_point)
    db.commit()
    db.refresh(starting_point)
    db.refresh(finishing_point)

    trip = Trip(
        passenger_limit=trip.passenger_limit,
        fare_per_person=trip.fare_per_person,
        route_url=trip.route_url,
        departure_datetime=trip.departure_datetime,
        driver_id=trip.driver_id,
        starting_point_id=starting_point.id,
        finishing_point_id=finishing_point.id,
        trip_status_id=trip.trip_status_id,
        vehicle_id=trip.vehicle_id
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return prepare_trip(trip)

@trip_router.post("/passenger", status_code=status.HTTP_201_CREATED)
def add_passenger_to_trip(trip_passenger: TripPassengerCreate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_passenger.trip_id).first()
    user = db.query(User).filter(User.id == trip_passenger.user_id).first()

    if trip is None or user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip or user not found")

    # Comprobar si el viaje ya está lleno
    if db.query(trip_passengers).filter(trip_passengers.c.trip_id == trip_passenger.trip_id).count() >= trip.passenger_limit:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trip is already full")
    
    if trip.trip_status.name != "Pending":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trip is not available for passengers")

    # Comprobar si el usuario ya está registrado en el viaje
    existing_passenger = db.query(trip_passengers).filter(
        trip_passengers.c.trip_id == trip_passenger.trip_id,
        trip_passengers.c.user_id == trip_passenger.user_id
    ).first()

    if existing_passenger is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a passenger in this trip")

    pick_up_stop = Stop(name=trip_passenger.pick_up_stop_name, latitude=trip_passenger.pick_up_stop_latitude, longitude=trip_passenger.pick_up_stop_longitude, description=trip_passenger.pick_up_stop_description)
    db.add(pick_up_stop)
    db.commit()
    db.refresh(pick_up_stop)

    try:
        db.execute(
            insert(trip_passengers).values(
                trip_id=trip_passenger.trip_id,
                user_id=trip_passenger.user_id,
                pickup_stop_id=pick_up_stop.id
            )
        )
        db.commit() 
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return {"detail": "Passenger added to trip successfully"}
