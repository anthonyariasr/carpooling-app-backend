from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import Vehicle, Trip, User

statistic_router = APIRouter()

@statistic_router.get("/statistic/institution/{institution_id}/total-trips", status_code=status.HTTP_200_OK)
def get_total_trips_by_institution(institution_id: int, db: Session = Depends(get_db)):
    # Consulta para contar el total de viajes asociados a los vehículos cuyos propietarios pertenecen a una institución
    total_trips = (
        db.query(Trip)
        .join(Vehicle)
        .join(User)
        .filter(User.institution_id == institution_id)
        .count()
    )

    if total_trips is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")

    return {"institution_id": institution_id, "total_trips": total_trips}

@statistic_router.get("/test")
def test_route():
    return {"message": "Router is working"}
