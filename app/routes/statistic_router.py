from sqlalchemy import func, and_, case
from typing import Optional, Dict
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
    total_passengers = (
        db.query(trip_passengers.c.user_id)
        .join(User, trip_passengers.c.user_id == User.id)
        .filter(User.institution_id == institution_id)
        .count()
    )

    # If no passengers are found for the institution, an error is thrown.
    if total_passengers == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found or has no passengers")

    return {"total_passengers": total_passengers}

#Total drivers by id institution
@statistic_router.get("/institution/{institution_id}/total-drivers", status_code=status.HTTP_200_OK)
def get_total_drivers_by_institution(institution_id: int, db: Session = Depends(get_db)):
    # We filter out users who are drivers in the institution
    driver_count = (
        db.query(User)
        .filter(User.institution_id == institution_id, User.user_type_id == 2)
        .count()
    )

    # We verify if there are drivers in the institution.
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

#New users by institution last week~month~year 
@statistic_router.get("/institution/{institution_id}/new-users", status_code=status.HTTP_200_OK)
def get_new_users_by_institution(institution_id: int, db: Session = Depends(get_db)):
    try:
        today = datetime.utcnow()
        last_week_date = today - timedelta(weeks=1)
        last_month_date = today - timedelta(days=30)
        last_year_date = today - timedelta(days=365)

        # Counting new users in the last week
        last_week_count = (
            db.query(User)
            .filter(User.institution_id == institution_id, User.date_registered >= last_week_date)
            .count()
        )

        # Count new users in the last month
        last_month_count = (
            db.query(User)
            .filter(User.institution_id == institution_id, User.date_registered >= last_month_date)
            .count()
        )

        # Count new users in the last year
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

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error fetching new users by institution")

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
    trips_by_gender = (
        db.query(
            Gender.id.label("id"),
            Gender.name.label("name"),
            func.count(Trip.id).label("total")
        )
        .select_from(Trip) 
        .join(User, Trip.driver_id == User.id)  # Join Trip with User in the driver relationship
        .join(Gender, User.gender_id == Gender.id)  # Join User with Gender
        .filter(User.institution_id == institution_id)  # Filter by institution
        .group_by(Gender.id, Gender.name)
        .all()
    )

    # Calculate the total number of trips
    total_trips = sum([row.total for row in trips_by_gender])

    if total_trips == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this institution")

    # Calculate percentages
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
@statistic_router.get("/institution/{institution_id}/average-trip-price", response_model=Dict[str, float])
def get_average_trip_price_by_institution(institution_id: int, db: Session = Depends(get_db)):
    average_price = (
        db.query(func.avg(Trip.fare_per_person).label("average"))
        .join(User, User.id == Trip.driver_id)  # Filter driver
        .filter(User.institution_id == institution_id)
        .scalar()  # Gets the scalar value directly
    )

    if average_price is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found or no trips available")

    return {"average": average_price}

#Total trips
@statistic_router.get("/total-trips", status_code=status.HTTP_200_OK)
def get_total_trips(db: Session = Depends(get_db)):
    total_trips = db.query(func.count(Trip.id)).scalar()

    # Check if trips exist in the database
    if total_trips is None or total_trips == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found")

    return {"total": total_trips}

#Total passengers (users) 
def get_total_passengers(db: Session = Depends(get_db)):
    try:
        total_passengers = db.query(User).count()  # Count all users
        return {"total": total_passengers}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error fetching total passengers")

#Total drivers 
def get_total_drivers(db: Session = Depends(get_db)):
    try:
        # Count distinct users who have been assigned as a driver in the Trip table
        total_drivers = db.query(func.count(User.id)).filter(Trip.driver_id == User.id).scalar()
        return {"total": total_drivers}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error fetching total drivers")

#Total institutions
@statistic_router.get("/total-institutions", status_code=status.HTTP_200_OK)
def get_total_institutions(db: Session = Depends(get_db)):
    total_institutions = db.query(func.count(Institution.id)).scalar()

    # Check if there are institutions in the database
    if total_institutions is None or total_institutions == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No institutions found")
    
    return {"total": total_institutions}

#Top users with the most trips as a driver
@statistic_router.get("/top-drivers", status_code=status.HTTP_200_OK)
def get_top_drivers(top: int, db: Session = Depends(get_db)):
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

    # Formatting the result
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
@statistic_router.get("/top-passengers", status_code=status.HTTP_200_OK)
def get_top_passengers(top: int = Query(1, gt=0, le=10), db: Session = Depends(get_db)):
    try:
        result = (
            db.query(
                User.id.label("id"),
                func.concat(User.first_name, ' ', User.first_surname).label("name"),
                func.count(trip_passengers.c.trip_id).label("total_of_trips")
            )
            .join(trip_passengers, trip_passengers.c.user_id == User.id)
            .group_by(User.id)
            .order_by(func.count(trip_passengers.c.trip_id).desc())
            .limit(top)
            .all()
        )

        # Transform the result into the expected response format.
        top_passengers = [
            {"id": user.id, "name": user.name, "total_of_trips": user.total_of_trips}
            for user in result
        ]

        return top_passengers

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Top institutions with the most users 1~3~5~10 
@statistic_router.get("/top-institutions", status_code=status.HTTP_200_OK)
def get_top_institutions(top: int = Query(1, gt=0, le=10), db: Session = Depends(get_db)):
    try:
        # Perform the query to obtain the institutions with the most users
        result = (
            db.query(
                Institution.id.label("id"),
                Institution.name.label("name"),
                func.count(User.id).label("user_total")
            )
            .join(User, User.institution_id == Institution.id)
            .group_by(Institution.id)
            .order_by(func.count(User.id).desc())
            .limit(top)
            .all()
        )

        # Transform the result into the expected response format.
        top_institutions = [
            {"id": institution.id, "name": institution.name, "user_total": institution.user_total}
            for institution in result
        ]

        return top_institutions

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
#Average trip price
@statistic_router.get("/average-trip-price", response_model=Dict[str, float])
def get_average_trip_price( db: Session = Depends(get_db)):
    average_price = (
        db.query(func.avg(Trip.fare_per_person).label("average"))
        .join(User, User.id == Trip.driver_id) 
        .scalar()  # Gets the scalar value directly
    )

    if average_price is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found or no trips available")

    return {"average": average_price}

#Trip percentage by gender (as passenger or driver)
@statistic_router.get("/trip-gender-percentage", status_code=status.HTTP_200_OK)
def get_trip_gender_percentage(db: Session = Depends(get_db)):

    trips_by_gender = (
        db.query(
            Gender.id.label("id"),
            Gender.name.label("name"),
            func.count(Trip.id).label("total")
        )
        .select_from(Trip)
        .join(User, Trip.driver_id == User.id)  # Join Trip with User in the driver relationship
        .join(Gender, User.gender_id == Gender.id)  # Join User with Gender
        .group_by(Gender.id, Gender.name)
        .all()
    )

    # Calculate the total number of trips
    total_trips = sum([row.total for row in trips_by_gender])

    if total_trips == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No trips found for this institution")

    # Calculate percentages
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
    
    # Calculate dates
    last_week = now - timedelta(weeks=1)
    last_month = now - timedelta(days=30)
    last_year = now - timedelta(days=365)
    
    # ID for completed travel status
    completed_status_id = 2
    
    # Queries for counting completed trips by institution and period
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
    
    # Response with total trips completed
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
    # Get current date
    today = date.today() 
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)
    one_year_ago = today - timedelta(days=365)

    # Queries to count new users on the specific dates
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