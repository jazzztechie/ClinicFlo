from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)  # "M" / "F" / "Other"
    phone = Column(String, nullable=False)

    appointments = relationship("Appointment", back_populates="patient")
    waitlist_entries = relationship("Waitlist", back_populates="patient")
