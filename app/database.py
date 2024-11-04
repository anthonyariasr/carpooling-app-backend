from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.base import Base
from dotenv import load_dotenv
import os

from app.models import *

# Cargar las variables del archivo .env
load_dotenv()

# Leer la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL_SQLITE")

# Crear el motor de base de datos
# Poner echo=True para ver SQL que sucede en la BD
engine = create_engine(DATABASE_URL, echo=True, pool_size=20, max_overflow=0)
Base.metadata.create_all(bind=engine)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
