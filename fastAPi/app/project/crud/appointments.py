from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..schemas import appointment

def create_appointment(db: Session, appointment: appointment.AppointmentCreate) -> models.Appointment:
    db_appointment = models.Appointment(doctor_id=appointment.doctor_id, notes=appointment.notes, patientname=appointment.patientname,date=appointment.date,time=appointment.time)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def appointment_response( db: Session, appointment: appointment.AppointmentResponse) -> models.Appointment:
    db_appointment = models.Appointment(date= appointment.date, time= appointment.time, notes=appointment.notes, patientname=appointment.patientname, doctor_id=appointment.doctor_id, patient_id=appointment.patient_id, id=appointment.id, status=appointment.status)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment_by_id(
    db: Session, doctor_id: Optional[int] = None, patientname: Optional[str] = None
) -> Optional[models.Appointment]:
    query = db.query(models.Appointment)
    
    if doctor_id:
        query = query.filter(models.Appointment.doctor_id == doctor_id)
    
    if patientname:
        query = query.filter(models.Appointment.patientname == patientname)
    
    return query.first()


# Get appointments by doctor ID
def get_appointments(db: Session, doctor_id: int, skip: int = 0, limit: int = 10) -> List[models.Appointment]:
    return db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id
    ).offset(skip).limit(limit).all()


# Delete appointment by patientname
def delete_appointment(db: Session, appointment_id: int, patientname: str) -> bool:
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id, 
        models.Appointment.patientname == patientname
    ).first()
    if appointment:
        db.delete(appointment)
        db.commit()
        return True
    return False
