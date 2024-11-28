from sqlalchemy import Column, Integer, ForeignKey, String, Date, Time, Text
from sqlalchemy.orm import relationship
from ..database import Base 

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    patientname = Column(String(50), nullable=False)
    status = Column(String(20), default="Pending")  
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])
