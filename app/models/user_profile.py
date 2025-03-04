from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base

class UserProfile(Base):
    __tablename__ = 'user_table'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)  
    email = Column(String, unique=True, nullable=True) 
    phone = Column(String, unique=True, nullable=False) 
    password_hash = Column(String, nullable=True)  
    created_at = Column(TIMESTAMP, server_default=func.now())
