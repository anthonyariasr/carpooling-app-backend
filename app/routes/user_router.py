from typing import List
from datetime import date
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import *
from app.schemas import *
from app.models import*
from app.schemas.user_schema import UserLogin, LoginResponse, UserUpdate
from app.tec_db import validate_user_tec  # Importa la función para validar el usuario en la base de datos tec
from app.interfaces import *

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
        "licence_plate": vehicle.license_plate,
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
@user_router.get("", response_model=List[UserResponse])
def get_all_users(institution_id: int = None, db: Session = Depends(get_db)):
    if institution_id is not None:
        users = db.query(User).filter(User.institution_id == institution_id).all()
    else: 
        users = db.query(User).all()
    return users

# Obtener la información de un usuario por ID
@user_router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return prepare_user(user)

# Obtener el numero de trips como driver de un user http://127.0.0.1:8000/users/users/2/driver-trips
@user_router.get("/{user_id}/driver-trips")
def get_driver_trips_count(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Contar el número de viajes como conductor
    driver_trips_count = len(user.trips_as_driver)

    return {"total": driver_trips_count}

# Vehiculos por usuario GET /users/1/vehicles
@user_router.get("/{user_id}/vehicles")
def get_vehicles_by_user(user_id: int, db: Session = Depends(get_db)):
    # Verifica si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Obtiene todos los vehículos del usuario
    vehicles = user.vehicles
    
    # Si no tiene vehículos
    if not vehicles:
        raise HTTPException(status_code=404, detail="No vehicles found for this user")
    
    formatted_vehicles = [prepare_vehicle(vehicle, user) for vehicle in vehicles]
    
    return formatted_vehicles

"""
# Login con email y contrasenna. esta leyendo la base que no es
@user_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.institutional_email == user_login.email).first()
    # Si no se encuentra el usuario o la contraseña es incorrecta
    # if not user or user.password != user_login.password:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Retornar el mensaje y el correo del usuario
    return {"message": "Login successful", "user": prepare_user(user)}

"""

@user_router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    try:
        # Use the Factory to select the authentication provider
        auth_provider = AuthFactory.get_auth_provider(user_login.email)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(e)})
    
    # Check if the user exists in the database
    user = db.query(User).filter(User.institutional_email == user_login.email).first()
    
    # Verify credentials with the specific provider
    if not user or not auth_provider.authenticate(user_login.email, user_login.password):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"})
    
    # Return the message and user data if authentication was successful
    return {"message": "Login successful", "user": prepare_user(user)}



# Registrar un nuevo usuario
@user_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print(f"Registrando nuevo usuario: {user}")

    user_exists = db.query(User).filter(User.institutional_email == user.institutional_email).first()
    
    if user_exists:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Correo electrónico ya registrado"}
        )
    
    try:
        print("Seleccionando el proveedor de autenticación...")
        # Use the Factory to select the authentication provider
        auth_provider = AuthFactory.get_auth_provider(user.institutional_email)
        if not auth_provider.check_existance(user.institutional_email):
            print(f"Error en la selección del proveedor") 
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Correo electrónico inválido"}
                )
    except ValueError as e:
        print("Error: El email no es válido según el proveedor de autenticación") 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Correo electrónico no peretenece a alguna institución registrada."}
        )
    
    print(f"Creando usuario: {user.dict()}")
    new_user = User(**user.dict())
    print(f"RRRRRRRRRRRRRRRRRRegistrando nuevo usuario: {user}")
    db.add(new_user)
    print(f"RegistrandoOOOOOOOOOOOOOOOOOOOOOOOOOO nuevo usuario: {user}")
    db.commit()
    print(f"Registrando NNNNNNNNNNNNNNNNNNNNNNNNNnuevo usuario: {user}")
    db.refresh(new_user)
    print("Usuario registrado exitosamente")
    return {"message": "Signup successful"}

# Regisrar el expiration date del divers license
@user_router.post("/{user_id}/license")
def register_license_expiration(user_id: int, expiration_date: date, db: Session = Depends(get_db)):
    # Verifica si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.dl_expiration_date = expiration_date
    
    db.commit()
    
    return {"message": "License expiration date updated successfully", "user_id": user.id, "expiration date": expiration_date}

# Eliminar un usuario por ID
@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@user_router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    for key, value in user.dict().items():
        if value is not None:
            setattr(user_db, key, value)
    
    db.commit()
    db.refresh(user_db)
    
    return prepare_user(user_db)

@user_router.put("/{user_id}/institution-admin", response_model=UserResponse, status_code=status.HTTP_200_OK)
def make_user_admin(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.user_type.name == "Institution-Admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already an institution admin")
    
    user_type = db.query(UserType).filter(UserType.name == "Institution-Admin").first()

    user.user_type_id = user_type.id
    
    db.commit()
    
    return prepare_user(user)

@user_router.delete("/{user_id}/institution-admin", response_model=UserResponse, status_code=status.HTTP_200_OK)
def remove_user_admin(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user_type = db.query(UserType).filter(UserType.name == "Base-User").first()

    user.user_type_id = user_type.id
    
    db.commit()
    
    return prepare_user(user)

@user_router.put("/{user_id}/rating/{rating}", status_code=status.HTTP_200_OK)
def rate_user(user_id: int, rating: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    current_rating = user.rating
    current_total_ratings = user.total_ratings
    
    new_rating = ((current_rating * current_total_ratings) + rating) / (current_total_ratings + 1)
    new_total_rating = current_total_ratings + 1

    user.rating = new_rating
    user.total_ratings = new_total_rating

    db.commit()
    
    return {"message": "User rated successfully", "user_id": user.id, "rating": user.rating}