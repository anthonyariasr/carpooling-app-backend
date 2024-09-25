from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from base import Base

class TripStatus(Base):
    __tablename__ = 'trip_status'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    trips = relationship("Trip", back_populates="trip_status")