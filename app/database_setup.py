#Ultima modificacion: 9/23/24 12:20 am

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Date, Table

# URL de conexión para PostgreSQL
DATABASE_URL = 'postgresql+psycopg2://postgres:123@localhost:5432/proyectoAP'

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()

trip_passengers = Table(
    'trip_passengers', Base.metadata, 
    Column('trip_id', ForeignKey('trip.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('pickup_stop_id', ForeignKey('stop.id'))
)
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    second_name = Column(String, nullable=True)
    first_surname = Column(String)
    second_surname = Column(String)

    identification = Column(Integer, index=True)
    birth_date = Column(Date)
    institutional_email = Column(String, index = True)
    phone_number = Column(String)
    dl_expiration_date = Column(Date)

    gender_id = Column(ForeignKey('gender.id'))
    gender = relationship('Gender', back_populates="users")

    user_type_id = Column(ForeignKey('user_type.id'))
    user_type = relationship('UserType', back_populates="users")

    institution_id = Column(ForeignKey('institution.id'))
    institution = relationship('Institution', back_populates="users")
    
    trips_as_driver = relationship('Trip', back_populates="driver")

    vehicles = relationship('Vehicle', back_populates="owner")

    trips_as_passenger = relationship("Trip", secondary=trip_passengers, back_populates="passengers")

class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    license_plate = Column(String, index=True)
    year = Column(String)
    max_capacity = Column(Integer)
    description = Column(String, nullable=True)

    owner_id = Column(ForeignKey('user.id'))
    owner = relationship("User", back_populates="vehicles")

    vehicle_type_id = Column(ForeignKey('vehicle_type.id'))
    vehicle_type = relationship('VehicleType', back_populates="vehicles")
   
    brand_id = Column(ForeignKey('brand.id'))
    brand = relationship('Brand', back_populates="vehicles")

    trips = relationship('Trip', back_populates = 'vehicle')

class VehicleType(Base):
    __tablename__ = 'vehicle_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    vehicles = relationship('Vehicle', back_populates='vehicle_type')

class Brand(Base):
    __tablename__  = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    vehicles = relationship("Vehicle", back_populates="brand")


class UserType(Base):
    __tablename__ = 'user_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('User', back_populates='user_type')
    
class Trip(Base):  
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    passenger_limit = Column(Integer)
    fare_per_person = Column(Integer)
    route_url = Column(String)
    departure_datetime = Column(DateTime)

    driver_id = Column(ForeignKey('user.id'))
    driver = relationship("User", back_populates="trips_as_driver")

    starting_point_id = Column(Integer, ForeignKey('stop.id'))
    starting_point = relationship("Stop", foreign_keys=[starting_point_id])

    finishing_point_id = Column(Integer, ForeignKey('stop.id'))
    finishing_point = relationship("Stop", foreign_keys=[finishing_point_id])
    
    trip_status_id = Column(ForeignKey('trip_status.id'))
    trip_status = relationship('TripStatus', back_populates="trips")

    vehicle_id = Column(ForeignKey('vehicle.id'))
    vehicle = relationship('Vehicle', back_populates="trips")
    
    passengers = relationship("User", secondary=trip_passengers, back_populates="trips_as_passenger")
    
class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)
    name = Column(String)
    description = Column(String, nullable=True)

class TripStatus(Base):
    __tablename__ = 'trip_status'
    id = Column(Integer, primary_key=True)
    name = Column(Integer)
    description = Column(String)

    trips = relationship("Trip", back_populates="trip_status")


class Institution(Base):
    __tablename__ = 'institution'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)

    users = relationship("User", back_populates = "institution")

class Gender(Base):
    __tablename__ = 'gender'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    users = relationship('User', back_populates = 'gender')


Base.metadata.create_all(bind=engine)


# Ejemplo de inserción de datos

new_brand = Brand(name="Toyota")
session.add(new_brand)
session.commit()

print(new_brand.id  + " : " + new_brand.name)
print("Todo bien")