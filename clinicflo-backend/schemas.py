"""
ClinicFlo - Pydantic schemas
All request/response validation lives here, kept separate from the
SQLAlchemy ORM models in models/.
"""
import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, Field, ConfigDict


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: str


# ---------------------------------------------------------------------------
# Patients
# ---------------------------------------------------------------------------
class PatientBase(BaseModel):
    name: str
    age: int = Field(..., ge=0, le=120)
    gender: Literal["M", "F", "Other"]
    phone: str


class PatientCreate(PatientBase):
    pass


class PatientOut(PatientBase):
    model_config = ConfigDict(from_attributes=True)
    patient_id: int


# ---------------------------------------------------------------------------
# Appointments
# ---------------------------------------------------------------------------
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: str
    appointment_date: datetime.date
    appointment_time: datetime.time
    status: Literal["scheduled", "completed", "cancelled", "no_show"] = "scheduled"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    doctor_id: Optional[str] = None
    appointment_date: Optional[datetime.date] = None
    appointment_time: Optional[datetime.time] = None
    status: Optional[Literal["scheduled", "completed", "cancelled", "no_show"]] = None
    risk_score: Optional[float] = None
    risk_level: Optional[Literal["LOW", "MEDIUM", "HIGH"]] = None


class AppointmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    appointment_id: int
    patient_id: int
    doctor_id: str
    appointment_date: datetime.date
    appointment_time: datetime.time
    booking_date: datetime.date
    status: str
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None


# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------
class PredictRequest(BaseModel):
    age: int = Field(..., ge=0, le=120)
    gender: Literal["M", "F", "Other"]
    scholarship: bool = Field(False, description="Enrolled in welfare/scholarship program")
    hypertension: bool = False
    diabetes: bool = False
    sms_received: bool = Field(False, description="Whether a reminder SMS was already sent")
    lead_time: int = Field(..., ge=0, description="Days between booking and appointment")
    appointment_id: Optional[int] = Field(
        None, description="If provided, the appointment's risk_score/risk_level are updated"
    )


class PredictResponse(BaseModel):
    probability: float
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    reasons: List[str]
    recommended_action: str


# ---------------------------------------------------------------------------
# Waitlist
# ---------------------------------------------------------------------------
class WaitlistBase(BaseModel):
    patient_id: int
    preferred_doctor: str
    preferred_date: datetime.date
    arrival_time: str = Field(..., description="Preferred time, e.g. '09:00'")
    priority: int = Field(1, ge=1, le=5, description="1=low urgency, 5=urgent")


class WaitlistCreate(WaitlistBase):
    pass


class WaitlistOut(WaitlistBase):
    model_config = ConfigDict(from_attributes=True)
    waitlist_id: int


class MatchSlotRequest(BaseModel):
    slot_id: int = Field(..., description="The freed-up appointment_id being reoffered")


class MatchSlotResponse(BaseModel):
    recommended_patient: Optional[WaitlistOut]
    reason: str
    runner_up_count: int = 0
