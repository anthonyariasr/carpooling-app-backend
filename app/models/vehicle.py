from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    license_plate = Column(String, index=True)
    year = Column(String)
    max_capacity = Column(Integer)
    description = Column(String, nullable=True)

    owner_id = Column(ForeignKey('user.id'))
    owner = relationship("User", "vehicles")