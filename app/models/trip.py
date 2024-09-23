from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Trip(Base):
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    passenger_limit = Column(Integer)
    
    driver_id = Column(ForeignKey('user.id'))
    driver = relationship("User", "trips_as_driver")