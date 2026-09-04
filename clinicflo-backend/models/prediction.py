import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.appointment_id"), nullable=True)
    probability = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    appointment = relationship("Appointment", back_populates="predictions")
