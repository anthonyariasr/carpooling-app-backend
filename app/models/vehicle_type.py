from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from base import Base

class VehicleType(Base):
    __tablename__ = 'vehicle_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    vehicles = relationship('Vehicle', back_populates='vehicle_type')