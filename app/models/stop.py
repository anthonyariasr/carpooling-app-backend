from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)
    name = Column(String)
    description = Column(String, nullable=True)