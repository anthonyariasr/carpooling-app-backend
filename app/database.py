from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.base import Base

from app.models import User
from app.models import Vehicle
from app.models import VehicleType
from app.models import Brand
from app.models import UserType
from app.models import Trip
from app.models import TripStatus
from app.models import Stop
from app.models import Institution
from app.models import Gender


DATABASE_URL_POSTGRES = 'postgresql+psycopg2://postgres:123@localhost:5432/proyectoAP'
DATABASE_URL_SQLITE = 'sqlite:///proyectoAP.db'


# Crear el motor de base de datos
engine = create_engine(DATABASE_URL_SQLITE, echo=True)
Base.metadata.create_all(bind=engine)

# Crear una fábrica de sesiones
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
