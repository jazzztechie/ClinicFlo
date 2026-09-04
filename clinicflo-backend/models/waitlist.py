from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Waitlist(Base):
    __tablename__ = "waitlist"

    waitlist_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    preferred_doctor = Column(String, nullable=False)
    preferred_date = Column(Date, nullable=False)
    arrival_time = Column(String, nullable=False)  # e.g. "09:00" - preferred time slot
    priority = Column(Integer, nullable=False, default=1)  # 1 (low) - 5 (urgent), user-set base urgency

    patient = relationship("Patient", back_populates="waitlist_entries")
