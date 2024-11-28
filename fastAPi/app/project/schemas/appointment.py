from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

# Schema for creating an appointment (data received from client)
class AppointmentCreate(BaseModel):
    doctor_id: int  # Doctor's ID (foreign key)
    date: date  # Appointment date
    time: time  # Appointment time
    notes: Optional[str] = Field(None, description="Additional notes for the appointment")

    class Config:
        from_attributes = True  # Replaced orm_mode with from_attributes

# Schema for reading an appointment (data sent to client)
class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: date
    time: time
    status: str  # 'Pending', 'Approved', 'Rejected'
    notes: Optional[str]

    class Config:
        from_attributes = True  # Replaced orm_mode with from_attributes

# Schema for updating an appointment's status
class AppointmentStatusUpdate(BaseModel):
    status: str  # New status: 'Pending', 'Approved', 'Rejected'

    class Config:
        from_attributes = True  # Replaced orm_mode with from_attributes
