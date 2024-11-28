from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

# Schema for creating an appointment (data received from client)
class AppointmentCreate(BaseModel):
    doctor_id: int  # Doctor's ID (foreign key)
    date: date  # Appointment date
    time: time  # Appointment time
    patientname: str
    notes: Optional[str] = Field(None, description="Additional notes for the appointment")

    class Config:
        from_attributes = True  # Replaced orm_mode with from_attributes

# Schema for reading an appointment (data sent to client)
# class AppointmentResponse(BaseModel):
#     id: int
#     patient_id: int
#     doctor_id: int
#     date: date
#     time: time
#     status: str  
#     patientname: str
#     notes: Optional[str]

#     class Config:
#         from_attributes = True  # Replaced orm_mode with from_attributes


class AppointmentResponse(AppointmentCreate):
    id: int
    patient_id: int
    status: str

    class Config:
        from_attributes = True

# Schema for updating an appointment's status
class AppointmentStatusUpdate(BaseModel):
    status: str  

    class Config:
        from_attributes = True  # Replaced orm_mode with from_attributes


# Schema for appointments (for listing appointments)
class AppointmentBase(BaseModel):
    doctor_id: int
    patientname: str
    date: date
    time: time
    status: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class Appointment(AppointmentBase):
    id: int
    status: str
    doctor_id: int
    patient_id: int

    class Config:
        from_attributes = True