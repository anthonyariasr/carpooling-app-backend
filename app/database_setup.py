from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean

# URL de conexión para PostgreSQL
DATABASE_URL = 'postgresql+psycopg2://postgres:123@localhost:5432/proyectoAP'

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    second_name = Column(String, nullable=True)
    first_surname = Column(String)
    second_surname = Column(String)

    identification = Column(Integer, index=True)
    birth_date = Column(DateTime)
    institutional_email = Column(String, index = True)
    phone_number = Column(String)
    dl_expiration_date = Column(DateTime)

    # Descripción: Esta línea define un atributo gender_id que actúa como una clave foránea en la tabla de User.
    # Relación: Este campo referencia el id de la tabla gender, lo que significa que cada usuario puede estar asociado a un género específico.
    gender_id = Column(ForeignKey('gender.id'))

    # Descripción: Cada instancia de User tendrá acceso a la instancia correspondiente de Gender a través de este atributo.
    # back_populates: Establece que en la clase Gender existe un atributo users que contiene todos los usuarios asociados a ese género.
    gender = relationship('Gender', back_populates="users")

    user_type_id = Column(ForeignKey('user_type.id'))
    user_type = relationship('UserType', back_populates="users")

    institution_id = Column(ForeignKey('institution.id'))
    institution = relationship('Institution', back_populates="users")
    
    trips_as_driver = relationship('Trip', back_populates="driver")

    # Un usuario puede poseer varios vehículos, y este atributo permitirá acceder a todos esos vehículos desde el objeto User.
    # back_populates: Este parametro establece que en la clase Vehicle existe un atributo owner que apunta a la instancia correspondiente de User
    vehicles = relationship('Vehicle', back_populates="owner")


class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    license_plate = Column(String, index=True)
    year = Column(String)
    max_capacity = Column(Integer)
    description = Column(String, nullable=True)

    owner_id = Column(ForeignKey('user.id'))
    owner = relationship("User", "vehicles")

class UserType(Base):
    __tablename__ = 'user_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('User', 'user_type')

class Trip(Base):
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    passenger_limit = Column(Integer)
    
    driver_id = Column(ForeignKey('user.id'))
    driver = relationship("User", "trips_as_driver")

class Institution(Base):
    __tablename__ = 'institution'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship("User", "institution")

class Gender(Base):
    __tablename__ = 'gender'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    users = relationship('User', 'gender')


Base.metadata.create_all(bind=engine)

print("Todo bien")