from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.database_setup import Brand

# URL de conexión para PostgreSQL
DATABASE_URL = 'postgresql+psycopg2://postgres:123@localhost:5432/proyectoAP'

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

connection = engine.connect()
print("Conexión exitosa")

# Crear una fábrica de sesiones
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()

Base.metadata.create_all(bind=engine)

print("Todo bien")


new_brand = Brand(name="Toyota")

session.add(new_brand)

session.commit()

