from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..schemas import appointment


def create_appointment(db: Session, appointment: appointment.AppointmentCreate) -> models.Appointment:
    db_appointment = models.Appointment(doctor_id=appointment.doctor_id, notes=appointment.notes,date=appointment.date,time=appointment.time)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def appointment_response( db: Session, appointment: appointment.AppointmentResponse) -> models.Appointment:
    db_appointment = models.Appointment(date= appointment.date, time= appointment.time, notes=appointment.notes, doctor_id=appointment.doctor_id, patient_id=appointment.patient_id, id=appointment.id, status=appointment.status)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def get_appointment_by_id(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def get_appointments(db: Session, skip: int = 0, limit: int = 10) -> List[models.Appointment]:
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def delete_appointment(db: Session, appointment_id: int) -> bool:
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appointment:
        db.delete(appointment)
        db.commit()
        return True
    return False
