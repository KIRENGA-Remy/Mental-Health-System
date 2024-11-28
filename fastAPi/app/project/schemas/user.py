from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid
from enum import Enum

class Role(str, Enum):
    patient = 'patient'
    doctor = 'doctor'

class UserCreate(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    role: Role

    class Config:
        from_attributes = True  # Replace orm_mode with from_attributes

class User(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True  # Replace orm_mode with from_attributes
