from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

# Base model for common appointment fields
class AppointmentBase(BaseModel):
    date: date
    time: time
    status: Optional[str] = "Pending"
    notes: Optional[str] = None

# Model for creating a new appointment (id is excluded)
class AppointmentCreate(AppointmentBase):
    doctor_id: int  # Add any additional fields specific to creation

# Model for returning appointment data (id is included)
class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    patientname: str

    class Config:
        from_attributes = True  # To support ORM objects and SQLAlchemy

# Schema for updating an appointment's status
class AppointmentStatusUpdate(BaseModel):
    status: str

    class Config:
        from_attributes = True
