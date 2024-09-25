from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

from .trip_passengers import trip_passengers
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
    
    passengers = relationship("User", secondary=lambda: trip_passengers, back_populates="trips_as_passenger")