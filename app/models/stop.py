from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base

class Stop(Base):
    __tablename__ = 'stop'
    id = Column(Integer, primary_key=True)
    latitude = Column(String)
    longitude = Column(String)
    name = Column(String, index=True)
    description = Column(String, nullable=True)