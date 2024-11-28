from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from project.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  
