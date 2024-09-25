from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from base import Base

class Institution(Base):
    __tablename__ = 'institution'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)

    users = relationship("User", back_populates = "institution")