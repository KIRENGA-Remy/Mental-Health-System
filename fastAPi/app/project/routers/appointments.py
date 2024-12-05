from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.appointment import AppointmentModel
from ..crud.appointments import get_appointment_by_id, get_appointments
from ..schemas.appointment import AppointmentCreate, AppointmentResponse
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

    return {
        "id": new_appointment.id,
        "date": new_appointment.date,
        "time": new_appointment.time,
        "status": new_appointment.status,
        "notes": new_appointment.notes,
        "patient_id": new_appointment.patient_id,
        "doctor_id": new_appointment.doctor_id,
        "patientname": new_appointment.patientname
    }


# Approve Appointment
@router.put("/approve/{appointment_id}", status_code=status.HTTP_200_OK)
async def approve_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ensure the current user is a doctor
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can approve appointments")

    # Retrieve the appointment
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Check if already approved
    if appointment.status == "Approved":
        raise HTTPException(status_code=400, detail="Appointment is already approved")
    
    # Ensure the doctor is assigned to this appointment
    if appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to approve this appointment")

    try:
        appointment.status = "Approved"
        db.commit()
        db.refresh(appointment)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while approving the appointment")
    
    return {
        "message": f"Appointment of {appointment.patientname} has been approved successfully.",
        "appointment": appointment
    }

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
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    if appointment.status == "Approved":
        raise HTTPException(status_code=400, detail="Appointment is already approved")
    
    # Ensure the doctor is assigned to this appointment
    if appointment.doctor_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to reject this appointment")

    # Update the status
    try:
        appointment.status = "Rejected"
        db.commit()
        db.refresh(appointment)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while rejecting the appointment")
    
    return {
        "message": f"Appointment of {appointment.patientname} has been rejected successfully.",
        "Appointment": appointment
    }


@router.get("/get_appointment/{appointment_id}", response_model=AppointmentResponse)
def get_appointment_by_id(
    appointment_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve appointment by ID
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Check access based on user role
    if current_user.role == "patient":
        if appointment.patient_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied: This appointment does not belong to you.")
    
    elif current_user.role == "doctor":
        if appointment.doctor_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied: You are not assigned to this appointment.")

    else:
        raise HTTPException(status_code=403, detail="Access denied: Invalid role.")

    return appointment


@router.delete("/delete_appointment/{appointment_id}", status_code=status.HTTP_200_OK)
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ensure only patients can delete appointments
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can delete their appointments")

    # Retrieve the appointment by ID
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Ensure the patient requesting deletion is the one who created the appointment
    if appointment.patient_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You can only delete your own appointments")

    # Delete the appointment
    try:
        db.delete(appointment)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the appointment")

    return {"message": "Appointment deleted successfully."}


#Retrieve all appointments without login in
router.get("/appointment", response_model=AppointmentResponse)
async def get_all_appointments(db: Session = Depends(get_db)):
    appointments = db.query(AppointmentModel).all()
    if not appointments:
        raise HTTPException(status_code=404,detail="No appointments found!")
    return appointments