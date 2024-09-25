from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import base

from models import User
from models import Vehicle
from models import VehicleType
from models import Brand
from models import UserType
from models import Trip
from models import TripStatus
from models import Stop
from models import Institution
from models import Gender


DATABASE_URL_POSTGRES = 'postgresql+psycopg2://postgres:123@localhost:5432/proyectoAP'
DATABASE_URL_SQLITE = 'sqlite:///proyectoAP.db'


# Crear el motor de base de datos
engine = create_engine(DATABASE_URL_SQLITE, echo=True)
base.Base.metadata.create_all(bind=engine)

# Crear una fábrica de sesiones
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

print("Todo bien")
