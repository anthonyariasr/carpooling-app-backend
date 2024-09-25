from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from base import Base

class Gender(Base):
    __tablename__ = 'gender'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    users = relationship('User', back_populates = 'gender')