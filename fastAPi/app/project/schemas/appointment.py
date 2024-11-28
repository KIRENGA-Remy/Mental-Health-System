from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

# Schema for creating an appointment (data received from client)
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


# Schema for updating an appointment's status
class AppointmentStatusUpdate(BaseModel):
    status: str  

    class Config:
        from_attributes = True  # Replaced orm_mode with from_attributes


# Schema for appointments (for listing appointments)
class AppointmentBase(BaseModel):
    date: date
    time: time
    patientname: str
    status: Optional[str] = "Pending"
    notes: Optional[str] = None

class Appointment(AppointmentBase):
    id: int
    doctor_id: int
    patient_id: int
    class Config:
        from_attributes = True

# Model used for creating a new appointment (id is excluded)
class AppointmentCreate(BaseModel): 
    date: date
    time: time
    status: Optional[str] = "Pending"
    notes: Optional[str] = None
    doctor_id: int

# Model used for returning appointment data (id is included)
class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    patientname: str

    class Config:
        from_attributes = True 
