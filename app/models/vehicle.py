from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base

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