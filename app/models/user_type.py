from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class UserType(Base):
    __tablename__ = 'user_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship('User', 'user_type')