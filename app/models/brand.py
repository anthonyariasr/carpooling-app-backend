from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.base import Base

class Brand(Base):
    __tablename__  = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    vehicles = relationship("Vehicle", back_populates="brand")