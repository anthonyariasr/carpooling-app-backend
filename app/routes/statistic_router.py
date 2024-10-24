from sqlalchemy import func, and_, case
from typing import Optional 
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import Vehicle, Trip, User, Institution, TripStatus, Gender

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

#Total passengers by id institution
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

#Total drivers by id-- FALTA
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


#Total trips completed within a period of one year~month~week
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

    # Consult the completed trips (status = 2)
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

#Trip percentage by gender (as passenger or driver) by institution
@statistic_router.get("/institution/{institution_id}/trips-by-gender", status_code=status.HTTP_200_OK)
def get_trips_by_gender(institution_id: int, db: Session = Depends(get_db)):
    # Definir explicitamente el punto de partida para el JOIN
    trips_by_gender = (
        db.query(
            Gender.id.label("id"),
            Gender.name.label("name"),
            func.count(Trip.id).label("total")
        )
        .select_from(Trip)  # Especificar la tabla de partida para evitar ambigüedad
        .join(User, Trip.driver_id == User.id)  # Unir Trip con User en la relación de conductores
        .join(Gender, User.gender_id == Gender.id)  # Unir User con Gender
        .filter(User.institution_id == institution_id)  # Filtrar por la institución
        .group_by(Gender.id, Gender.name)
        .all()
    )

    # Calcular el total de viajes
    total_trips = sum([row.total for row in trips_by_gender])

    if total_trips == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this institution")

    # Calcular los porcentajes
    result = [
        {
            "id": row.id,
            "name": row.name,
            "total": row.total,
            "percentage": round((row.total / total_trips) * 100, 2)
        }
        for row in trips_by_gender
    ]

    return result

#Average trip price by institution
#Total trips
@statistic_router.get("/total-trips", status_code=status.HTTP_200_OK)
def get_total_trips(db: Session = Depends(get_db)):
    # Consulta para contar el total de viajes
    total_trips = db.query(func.count(Trip.id)).scalar()

    # Verificar si existen viajes en la base de datos
    if total_trips is None or total_trips == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found")

    # Retornar el total en el formato requerido
    return {"total": total_trips}

#Total passengers (users)
#Total drivers
#Total institutions
@statistic_router.get("/total-institutions", status_code=status.HTTP_200_OK)
def get_total_institutions(db: Session = Depends(get_db)):
    # Consulta para contar el total de instituciones
    total_institutions = db.query(func.count(Institution.id)).scalar()

    # Verificar si existen instituciones en la base de datos
    if total_institutions is None or total_institutions == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No institutions found")

    # Retornar el total en el formato requerido
    return {"total": total_institutions}

#Top users with the most trips as a driver
@statistic_router.get("/top-drivers", status_code=status.HTTP_200_OK)
def get_top_drivers(top: int, db: Session = Depends(get_db)):
    # Consulta para obtener los conductores con más viajes
    top_drivers = (
        db.query(
            User.id.label("id"),
            func.concat(User.first_name, " ", User.first_surname).label("name"),
            func.count(Trip.id).label("total_of_trips")
        )
        .join(Trip, Trip.driver_id == User.id)
        .group_by(User.id, User.first_name, User.first_surname)
        .order_by(func.count(Trip.id).desc())
        .limit(top)
        .all()
    )

    if not top_drivers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No drivers found")

    # Formatear el resultado
    result = [
        {
            "id": driver.id,
            "name": driver.name,
            "total_of_trips": driver.total_of_trips
        }
        for driver in top_drivers
    ]

    return result


#Top users with the most trips as a passenger
#Top institutions with the most users
#Average trip price
#Trip percentage by gender (as passenger or driver)
#Completed trips in the last week, month, and year (by institution)
#Trip percentage by gender (as passenger or driver) by institution
@statistic_router.get("/trip-gender-percentage", status_code=status.HTTP_200_OK)
def get_trip_gender_percentage(db: Session = Depends(get_db)):
    # Definir explicitamente el punto de partida para el JOIN
    trips_by_gender = (
        db.query(
            Gender.id.label("id"),
            Gender.name.label("name"),
            func.count(Trip.id).label("total")
        )
        .select_from(Trip)  # Especificar la tabla de partida para evitar ambigüedad
        .join(User, Trip.driver_id == User.id)  # Unir Trip con User en la relación de conductores
        .join(Gender, User.gender_id == Gender.id)  # Unir User con Gender
        .group_by(Gender.id, Gender.name)
        .all()
    )

    # Calcular el total de viajes
    total_trips = sum([row.total for row in trips_by_gender])

    if total_trips == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this institution")

    # Calcular los porcentajes
    result = [
        {
            "id": row.id,
            "name": row.name,
            "total": row.total,
            "percentage": round((row.total / total_trips) * 100, 2)
        }
        for row in trips_by_gender
    ]

    return result

#New users in the last week, month, and year-- CONSULTAR
@statistic_router.get("/new-users", status_code=status.HTTP_200_OK)
def get_new_users(db: Session = Depends(get_db)):
    # Obtener la fecha actual
    today = date.today()  # Cambiado a `date.today()` para manejar solo fechas
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)
    one_year_ago = today - timedelta(days=365)

    # Consultas para contar usuarios nuevos en las fechas específicas
    last_week = db.query(func.count(User.id)).filter(User.date_registered >= one_week_ago).scalar()
    last_month = db.query(func.count(User.id)).filter(User.date_registered >= one_month_ago).scalar()
    last_year = db.query(func.count(User.id)).filter(User.date_registered >= one_year_ago).scalar()

    if last_week is None and last_month is None and last_year is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No new users found")

    return {
        "last_week": last_week,
        "last_month": last_month,
        "last_year": last_year
    }