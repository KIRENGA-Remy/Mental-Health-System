# from sqlalchemy import Column, Integer, ForeignKey, String, Date, Time, Text
# from sqlalchemy.orm import relationship
# from ..database import Base 

# class AppointmentModel(Base):
#     __tablename__ = "appointments"

#     id = Column(Integer, primary_key=True, index=True)
#     patient_id = Column(Integer, ForeignKey("users.id"))
#     doctor_id = Column(Integer, ForeignKey("users.id"))
#     date = Column(Date, nullable=False)
#     time = Column(Time, nullable=False)
#     patientname = Column(String(50), nullable=False)
#     status = Column(String(20), default="Pending")  
#     notes = Column(Text, nullable=True)

#     # Relationships
#     patient = relationship("User", foreign_keys=[patient_id])
#     doctor = relationship("User", foreign_keys=[doctor_id])











from sqlalchemy import Column, Integer, ForeignKey, String, Date, Time, Text
from sqlalchemy.orm import relationship
from ..database import Base

class AppointmentModel(Base):
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
    
    # Add this method to convert the model into a dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": str(self.date),  # Convert date to string
            "time": str(self.time),  # Convert time to string
            "patientname": self.patientname,
            "status": self.status,
            "notes": self.notes
        }
