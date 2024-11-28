from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.appointment import Appointment
from ..models.user import User
from ..crud.appointments import get_appointment_by_id, get_appointments
from ..schemas.appointment import AppointmentCreate, AppointmentResponse, Appointment
from ..utils import get_current_user
from ..database import get_db
from typing import Optional

router = APIRouter()

@router.post("/request_appointment/", response_model=AppointmentResponse)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure only patients can create appointments
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can request appointments")

    # Check if doctor exists
    doctor = db.query(User).filter(User.id == appointment_data.doctor_id, User.role == "doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Create appointment
    new_appointment = Appointment(
        patient_id=current_user.id,
        doctor_id=doctor.id,
        date=appointment_data.date,
        time=appointment_data.time,
        patientname=current_user.username,
        notes=appointment_data.notes
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment  


# Approve Appointment
@router.put("/approve/{appointment_id}", status_code=status.HTTP_200_OK)
async def approve_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the current user is a doctor
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can approve appointments")

    # Retrieve the appointment
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Ensure the doctor is assigned to this appointment
    if appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to approve this appointment")

    # Update the status
    appointment.status = "Approved"
    db.commit()
    db.refresh(appointment)
    
    return {"message": f"Appointment of {appointment.patientname} has been approved successfully."}

# Reject Appointment
@router.put("/reject/{appointment_id}", status_code=status.HTTP_200_OK)
async def reject_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the current user is a doctor
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can reject appointments")

    # Retrieve the appointment
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Ensure the doctor is assigned to this appointment
    if appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to reject this appointment")

    # Update the status
    appointment.status = "Rejected"
    db.commit()
    db.refresh(appointment)
    
    return {"message": f"Appointment of {appointment.patientname} has been rejected successfully."}


@router.get("/get_appointment/{appointment_id}", response_model=Appointment)
def get_appointment_by_id(
    appointment_id: int, 
    doctor_id: Optional[int] = None, 
    patientname: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Retrieve appointment by doctor_id or patientname or both
    appointment = get_appointment_by_id(db, doctor_id=doctor_id, patientname=patientname)
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return appointment