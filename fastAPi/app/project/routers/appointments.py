from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.appointment import AppointmentModel
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
    
    # Extract patientname from current_user
    patient_name = current_user.username

    # Create appointment using current_user's name
    new_appointment = AppointmentModel(
        date=appointment_data.date,
        time=appointment_data.time,
        status=appointment_data.status,
        patientname=patient_name,
        notes=appointment_data.notes,
        doctor_id=appointment_data.doctor_id,
        patient_id=current_user.id
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve appointment by ID
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Ensure patient or assigned doctor can view it
    if current_user.role == "patient" and appointment.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user.role == "doctor" and appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return appointment
