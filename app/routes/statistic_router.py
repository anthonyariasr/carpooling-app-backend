from sqlalchemy import func, and_
from typing import Optional 
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import Vehicle, Trip, User, Institution, TripStatus

statistic_router = APIRouter()

#Total trips by id institucion
@statistic_router.get("/institution/{institution_id}/total-trips", status_code=status.HTTP_200_OK)
def get_total_trips_by_institution(institution_id: int, db: Session = Depends(get_db)):
    total_trips = (
        db.query(Trip)
        .join(Vehicle)
        .join(User)
        .filter(User.institution_id == institution_id)
        .count()
    )

    if total_trips is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")

    return {"total_trips": total_trips}

#Total passengers by id--
@statistic_router.get("/institution/{institution_id}/total-passengers", status_code=status.HTTP_200_OK)
def get_total_passengers_by_institution(institution_id: int, db: Session = Depends(get_db)):
    total_trips = (
        db.query(User)
        .filter(User.institution_id == institution_id)
        .count()
    )

    if total_trips is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")

    return {"total_passegers": total_trips}

#Driver by id-- FALTA
@statistic_router.get("/institution/{institution_id}/total-passengers", status_code=status.HTTP_200_OK)
def get_total_passengers_by_institution(institution_id: int, db: Session = Depends(get_db)):
    # Consulta para contar el total de viajes asociados a los vehículos cuyos propietarios pertenecen a una institución
    total_trips = (
        db.query(User)
        .filter(User.institution_id == institution_id)
        .count()
    )

    if total_trips is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")

    return {"total_passegers": total_trips}

#Top user by institution 1~5
@statistic_router.get("/top-institutions", status_code=status.HTTP_200_OK)
def get_top_institutions(top: int = 5, db: Session = Depends(get_db)):
    top_institutions = (
        db.query(Institution.id, Institution.name, func.count(User.id).label("user_total"))
        .join(User)
        .group_by(Institution.id, Institution.name)
        .order_by(func.count(User.id).desc())
        .limit(top)
        .all()
    )

    if not top_institutions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No institutions found")

    return [{"id": inst.id, "name": inst.name, "user_total": inst.user_total} for inst in top_institutions]


#total trips completed within a period of one year~month~week
@statistic_router.get("/institution/{institution_id}/completed-trips", status_code=status.HTTP_200_OK)
def get_completed_trips_by_institution(institution_id: int, period: Optional[str] = "week", db: Session = Depends(get_db)):
    # Define the cut-off date according to the period
    today = datetime.today()
    
    if period == "week":
        start_date = today - timedelta(weeks=1)
    elif period == "month":
        start_date = today - timedelta(days=30)
    elif period == "year":
        start_date = today - timedelta(days=365)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid period. Choose 'week', 'month', or 'year'.")

    # Consultar los viajes completados (estado = 2)
    completed_trips = (
        db.query(func.count(Trip.id))
        .join(User, Trip.driver_id == User.id)
        .filter(
            and_(
                User.institution_id == institution_id,
                Trip.trip_status_id == 2,  # Status 'Completed' = 2
                Trip.departure_datetime >= start_date
            )
        )
        .scalar()
    )

    if completed_trips is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this institution.")

    return {"total": completed_trips}

