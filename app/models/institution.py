from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Institution(Base):
    __tablename__ = 'institution'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship("User", "institution")