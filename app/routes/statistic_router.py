from sqlalchemy import func, and_, case
from typing import Optional, List, Dict
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.database import get_db
from app.models import Vehicle, Trip, User, Institution, TripStatus, Gender, trip_passengers
from app.schemas.user_schema import UserBasicInfo
from app.schemas import GenderResponse

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
    # Realizamos un join entre trip_passengers y User, utilizando trip_passengers.c.user_id
    total_passengers = (
        db.query(trip_passengers.c.user_id)
        .join(User, trip_passengers.c.user_id == User.id)
        .filter(User.institution_id == institution_id)
        .count()
    )

    # Si no se encuentran pasajeros para la institución, lanzamos un error
    if total_passengers == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found or has no passengers")

    return {"total_passengers": total_passengers}

#Total drivers by id institution
@statistic_router.get("/institution/{institution_id}/total-drivers", status_code=status.HTTP_200_OK)
def get_total_drivers_by_institution(institution_id: int, db: Session = Depends(get_db)):
    # Filtramos los usuarios que son conductores en la institución
    driver_count = (
        db.query(User)
        .filter(User.institution_id == institution_id, User.user_type_id == 2)
        .count()
    )

    # Verificamos si existen conductores en la institución
    if driver_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No drivers found for this institution")

    return {"total": driver_count}

#Total trips completed with period of one year~month~week
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

#New users by institution last week~month~year --CONSULTAR
@statistic_router.get("/institution/{institution_id}/new-users", status_code=status.HTTP_200_OK)
def get_new_users_by_institution(institution_id: int, db: Session = Depends(get_db)):
    today = datetime.utcnow()
    last_week_date = today - timedelta(weeks=1)
    last_month_date = today - timedelta(days=30)
    last_year_date = today - timedelta(days=365)

    # Contar nuevos usuarios en la última semana
    last_week_count = (
        db.query(User)
        .filter(User.institution_id == institution_id, User.date_registered >= last_week_date)
        .count()
    )

    # Contar nuevos usuarios en el último mes
    last_month_count = (
        db.query(User)
        .filter(User.institution_id == institution_id, User.date_registered >= last_month_date)
        .count()
    )

    # Contar nuevos usuarios en el último año
    last_year_count = (
        db.query(User)
        .filter(User.institution_id == institution_id, User.date_registered >= last_year_date)
        .count()
    )

    return {
        "last_week": last_week_count,
        "last_month": last_month_count,
        "last_year": last_year_count
    }

#Top passengers with the most trips by institution 1~3~5~10
@statistic_router.get("/institution/{institution_id}/top-passengers", status_code=status.HTTP_200_OK)
def get_top_passengers_by_institution(institution_id: int, top: int = Query(5, ge=1, le=10), db: Session = Depends(get_db)):
    top_passengers = (
        db.query(
            User.id,
            User.first_name,
            User.first_surname,
            func.count(trip_passengers.user_id).label("total_of_trips")
        )
        .join(trip_passengers, trip_passengers.user_id == User.id)
        .join(Trip, Trip.id == trip_passengers.trip_id)
        .filter(User.institution_id == institution_id)
        .group_by(User.id)
        .order_by(func.count(trip_passengers.user_id).desc())
        .limit(top)
        .all()
    )

    if not top_passengers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No passengers found for this institution")

    return [
        {
            "id": passenger.id,
            "name": f"{passenger.first_name} {passenger.first_surname}",
            "total_of_trips": passenger.total_of_trips
        } for passenger in top_passengers
    ]

#Top drivers with the most trips by institution 1~3~5~10
@statistic_router.get("/institution/{institution_id}/top-drivers", status_code=status.HTTP_200_OK)
def get_top_drivers_by_institution(institution_id: int, top: int = Query(5, ge=1, le=10), db: Session = Depends(get_db)):
    top_drivers = (
        db.query(
            User.id,
            User.first_name,
            User.first_surname,
            func.count(Trip.id).label("total_of_trips")
        )
        .join(Trip, Trip.driver_id == User.id)
        .filter(User.institution_id == institution_id)
        .group_by(User.id)
        .order_by(func.count(Trip.id).desc())
        .limit(top)
        .all()
    )

    if not top_drivers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No drivers found for this institution")

    return [
        {
            "id": driver.id,
            "name": f"{driver.first_name} {driver.first_surname}",
            "total_of_trips": driver.total_of_trips
        } for driver in top_drivers
    ]

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

#Average trip price by institution --CONSULTAR
@statistic_router.get("/institution/{institution_id}/average-trip-price", response_model=Dict[str, float])
def get_average_trip_price_by_institution(institution_id: int, db: Session = Depends(get_db)):
    # Consulta para obtener el precio promedio de los viajes para la institución
    average_price = (
        db.query(func.avg(Trip.fare_per_person).label("average"))
        .join(User, User.id == Trip.driver_id)  # Asegúrate de ajustar esto según tu modelo de Trip
        .filter(User.institution_id == institution_id)
        .scalar()  # Obtiene el valor escalar directamente
    )

    if average_price is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found or no trips available")

    return {"average": average_price}

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

#Total passengers (users) --CONSULTAR
@statistic_router.get("/total-passengers", response_model=Dict[str, int])
def get_total_passengers(db: Session = Depends(get_db)):
    # Consulta para obtener el total de pasajeros
    total_passengers = db.query(User).count()  # Cuenta todos los usuarios

    return {"total": total_passengers}

#Total drivers
@statistic_router.get("/total-drivers")
def get_total_drivers(db: Session = Depends(get_db)):
    # Contar los usuarios que tienen el rol de conductor
    total_drivers = db.query(func.count(User.id)).filter(User.user_type_id == 2).scalar()

    return {"total": total_drivers}

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

 
#Top users with the most trips as a passenger-- NO FUNCIONA
@statistic_router.get("/top-passengers", response_model=List[UserBasicInfo], status_code=status.HTTP_200_OK)
def get_top_passengers(top: int, db: Session = Depends(get_db)):
    top_passengers = (
        db.query(
            User.id,
            User.first_name,
            User.first_surname,
            func.count(trip_passengers.id).label("total_of_trips")
        )
        .join(trip_passengers, trip_passengers.user_id == User.id)  # Relación usuario y pasajero
        .group_by(User.id, User.first_name, User.first_surname)
        .order_by(func.count(trip_passengers.trip_id).desc())
        .limit(top)
        .all()
    )

    if not top_passengers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No passengers found with trips")

    # Construcción de respuesta con el formato especificado
    result = [
        {
            "id": passenger.id,
            "name": f"{passenger.first_name} {passenger.first_surname}",
            "total_of_trips": passenger.total_of_trips
        }
        for passenger in top_passengers
    ]

    return result

# Top institutions with the most users 1~3~5~10 --NO FUNCIONA
@statistic_router.get("/top-institutions", response_model=List[Dict[str, int]])
def get_top_institutions(top: int = 10, db: Session = Depends(get_db)):
    # Consulta para obtener las instituciones con más usuarios
    top_institutions_raw = (
        db.query(
            Institution.id,
            Institution.name,
            func.count(User.id).label("user_total")
        )
        .join(User, User.institution_id == Institution.id)
        .group_by(Institution.id, Institution.name)
        .order_by(func.count(User.id).desc())
        .limit(top)
        .all()
    )

    # Transformamos los resultados en el formato adecuado
    top_institutions = [
        {"id": inst_id, "name": inst_name, "user_total": user_total}
        for inst_id, inst_name, user_total in top_institutions_raw
    ]

    if not top_institutions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No institutions found")

    return top_institutions

#Average trip price
@statistic_router.get("/average-trip-price", response_model=Dict[str, float])
def get_average_trip_price( db: Session = Depends(get_db)):
    # Consulta para obtener el precio promedio de los viajes para la institución
    average_price = (
        db.query(func.avg(Trip.fare_per_person).label("average"))
        .join(User, User.id == Trip.driver_id)  # Asegúrate de ajustar esto según tu modelo de Trip
        .scalar()  # Obtiene el valor escalar directamente
    )

    if average_price is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found or no trips available")

    return {"average": average_price}

#Trip percentage by gender (as passenger or driver)
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

#Completed trips in the last week, month, and year (by institution)
@statistic_router.get("/completed-trips", status_code=status.HTTP_200_OK)
def get_completed_trips_by_institution(id_institution: int, db: Session = Depends(get_db)):
    now = datetime.now()
    
    # Calcular fechas
    last_week = now - timedelta(weeks=1)
    last_month = now - timedelta(days=30)
    last_year = now - timedelta(days=365)
    
    # ID para el estado de viaje completado
    completed_status_id = 2
    
    # Consultas para contar viajes completados por institución y período
    last_week_trips = db.query(func.count(Trip.id)).join(User, Trip.driver_id == User.id).filter(
        User.institution_id == id_institution,
        Trip.trip_status_id == completed_status_id,
        Trip.departure_datetime >= last_week
    ).scalar()
    
    last_month_trips = db.query(func.count(Trip.id)).join(User, Trip.driver_id == User.id).filter(
        User.institution_id == id_institution,
        Trip.trip_status_id == completed_status_id,
        Trip.departure_datetime >= last_month
    ).scalar()
    
    last_year_trips = db.query(func.count(Trip.id)).join(User, Trip.driver_id == User.id).filter(
        User.institution_id == id_institution,
        Trip.trip_status_id == completed_status_id,
        Trip.departure_datetime >= last_year
    ).scalar()
    
    # Respuesta con el total de viajes completados
    response = {
        "last_week": last_week_trips,
        "last_month": last_month_trips,
        "last_year": last_year_trips
    }
    
    if all(value == 0 for value in response.values()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No completed trips found for this institution"
        )
    
    return response


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