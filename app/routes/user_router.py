from typing import List
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database import *
from app.schemas import *
from app.models import*
from app.schemas.user_schema import UserLogin, LoginResponse
from app.tec_db import validate_user_tec  # Importa la función para validar el usuario en la base de datos tec

user_router = APIRouter()

def prepare_user(user: User):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "first_surname": user.first_surname,
        "second_surname": user.second_surname,
        "identification": user.identification,
        "birth_date": user.birth_date,
        "institutional_email": user.institutional_email,
        "phone_number": user.phone_number,
        "dl_expiration_date": user.dl_expiration_date,
        "rating": user.rating,
        "date_registered": user.date_registered,
        "total_ratings": user.total_ratings,
        "user_type": {
            "id": user.user_type.id,
            "name": user.user_type.name
        },
        "gender": {
            "id": user.gender.id,
            "name": user.gender.name
        },
        "institution": {
            "id": user.institution.id,
            "name": user.institution.name,
            "acronym": user.institution.acronym
        },
    }

def prepare_vehicle(vehicle, owner):
    return {
        "id": vehicle.id,
        "licence_plate": vehicle.licence_plate,
        "year": vehicle.year,
        "max_capacity": vehicle.max_capacity,
        "description": vehicle.description,
        "owner": {
            "id": owner.id,
            "name": f"{owner.first_name} {owner.first_surname}"
        },
        "vehicle_type": {
            "id": vehicle.vehicle_type.id,
            "name": vehicle.vehicle_type.name
        },
        "brand": {
            "id": vehicle.brand.id,
            "name": vehicle.brand.name
        }
    }

# obtener todos los usuarios 
@user_router.get("/users", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Obtener la información de un usuario por ID
@user_router.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return prepare_user(user)

# Obtener el numero de trips como driver de un user http://127.0.0.1:8000/users/users/2/driver-trips
@user_router.get("/users/{user_id}/driver-trips")
def get_driver_trips_count(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Contar el número de viajes como conductor
    driver_trips_count = len(user.trips_as_driver)

    return {"total": driver_trips_count}

# Vehiculos por usuario GET /users/vehicles?user_id=1
@user_router.get("/vehicles")
def get_vehicles_by_user(user_id: int, db: Session = Depends(get_db)):
    # Verifica si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Obtiene todos los vehículos del usuario
    vehicles = db.query(Vehicle).filter(Vehicle.owner_id == user_id).all()
    
    # Si no tiene vehículos
    if not vehicles:
        raise HTTPException(status_code=404, detail="No vehicles found for this user")
    
    formatted_vehicles = [prepare_vehicle(vehicle, user) for vehicle in vehicles]
    
    return formatted_vehicles

# Login con email y contrasenna. esta leyendo la base que no es
@user_router.post("/users/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    
    # Si no se encuentra el usuario o la contraseña es incorrecta
    if not user or user.password != user_login.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Retornar el mensaje y el correo del usuario
    return {"message": "Login successful", "user_email": user.email}

# Registrar un nuevo usuario
@user_router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Regisrar el expiration date del divers license
@user_router.post("/users/{user_id}/license")
def register_license_expiration(user_id: int, expiration_date: date, db: Session = Depends(get_db)):
    # Verifica si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.dl_expiration_date = expiration_date
    
    db.commit()
    
    return {"message": "License expiration date updated successfully", "user_id": user.id, "expiration date": expiration_date}

# Eliminar un usuario por ID
@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}