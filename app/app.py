from typing import List, Optional
from datetime import date, time
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from app.database import *
from app.schemas import *

from app.routes import trip_router 

app = FastAPI()

app.include_router(trip_router, prefix="/trips")

@app.get("/")
def is_running():
    return {"running": True}

@app.get("/users")
def get_users():
    users = session.query(User).all()
    users_dict = [user_to_dict(user) for user in users]
    return users_dict


# Función para convertir una instancia de User a diccionario
def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.first_name,
        'lastname': user.first_surname
    }
