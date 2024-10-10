from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Date, CheckConstraint, DECIMAL
from sqlalchemy.orm import relationship
from app.base import Base

from .trip_passengers import trip_passengers
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
    date_registered = Column(Date)
    rating = Column(DECIMAL, CheckConstraint('rating >= 1.0 AND rating <= 5.0'))

    gender_id = Column(ForeignKey('gender.id'))
    gender = relationship('Gender', back_populates="users")

    user_type_id = Column(ForeignKey('user_type.id'))
    user_type = relationship('UserType', back_populates="users")

    institution_id = Column(ForeignKey('institution.id'))
    institution = relationship('Institution', back_populates="users")
    
    trips_as_driver = relationship('Trip', back_populates="driver")

    vehicles = relationship('Vehicle', back_populates="owner")

    trips_as_passenger = relationship("Trip", secondary=lambda: trip_passengers, back_populates="passengers")