from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""Esto es un código de ejemplo para usar como base"""

# URL de conexión para PostgreSQL
DATABASE_URL = "postgresql+psycopg2://username:password@rds-endpoint:5432/dbname" #Acá hay que usar variables de entorno e idealmente usar la DB hosteada en algún lado como AWS RDS

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear una clase base para los modelos
Base = declarative_base()

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
