import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.appointment import Appointment
from models.patient import Patient
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentOut])
def list_appointments(
    status: str | None = None,
    doctor_id: str | None = None,
    db: Session = Depends(get_db),
):
    """
    List appointments, optionally filtered by status and/or doctor_id.
    Frontend can poll this endpoint (no WebSockets needed for the demo).
    """
    query = db.query(Appointment)
    if status:
        query = query.filter(Appointment.status == status)
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    return query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if appt is None:
        raise HTTPException(status_code=404, detail=f"Appointment {appointment_id} not found")
    return appt


@router.post("", response_model=AppointmentOut, status_code=201)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == payload.patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail=f"Patient {payload.patient_id} not found")

    appt = Appointment(
        **payload.model_dump(),
        booking_date=datetime.date.today(),
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, payload: AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if appt is None:
        raise HTTPException(status_code=404, detail=f"Appointment {appointment_id} not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appt, field, value)

    db.commit()
    db.refresh(appt)
    return appt
