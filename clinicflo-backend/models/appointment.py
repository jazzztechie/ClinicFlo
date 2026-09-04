import datetime

from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(String, nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    booking_date = Column(Date, nullable=False, default=datetime.date.today)
    status = Column(String, nullable=False, default="scheduled")
    # scheduled | completed | cancelled | no_show

    risk_score = Column(Float, nullable=True)  # last predicted probability
    risk_level = Column(String, nullable=True)  # LOW | MEDIUM | HIGH

    patient = relationship("Patient", back_populates="appointments")
    predictions = relationship("Prediction", back_populates="appointment")
