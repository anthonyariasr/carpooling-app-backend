from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

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

    gender_id = Column(ForeignKey('gender.id'))
    gender = relationship('Gender', back_populates="users")

    user_type_id = Column(ForeignKey('user_type.id'))
    user_type = relationship('UserType', back_populates="users")

    institution_id = Column(ForeignKey('institution.id'))
    institution = relationship('Institution', back_populates="users")
    
    trips_as_driver = relationship('Trip', back_populates="driver")

    vehicles = relationship('Vehicle', back_populates="owner")