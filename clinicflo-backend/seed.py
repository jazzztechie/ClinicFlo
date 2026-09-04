"""
ClinicFlo - Demo data seeding

Populates a handful of patients, appointments, and waitlist entries so the
frontend has something to render immediately. Idempotent: skips seeding if
patients already exist.
"""
import datetime

from sqlalchemy.orm import Session

from models.patient import Patient
from models.appointment import Appointment
from models.waitlist import Waitlist


def seed_if_empty(db: Session):
    if db.query(Patient).count() > 0:
        return  # Already seeded.

    today = datetime.date.today()

    patients = [
        Patient(name="Asha Verma", age=29, gender="F", phone="9876500001"),
        Patient(name="Ravi Kumar", age=45, gender="M", phone="9876500002"),
        Patient(name="Meera Iyer", age=62, gender="F", phone="9876500003"),
        Patient(name="Sanjay Patel", age=34, gender="M", phone="9876500004"),
        Patient(name="Priya Nair", age=8, gender="F", phone="9876500005"),
        Patient(name="Kabir Shah", age=51, gender="M", phone="9876500006"),
    ]
    db.add_all(patients)
    db.commit()
    for p in patients:
        db.refresh(p)

    appointments = [
        Appointment(
            patient_id=patients[0].patient_id,
            doctor_id="DR-101",
            appointment_date=today + datetime.timedelta(days=2),
            appointment_time=datetime.time(9, 30),
            booking_date=today - datetime.timedelta(days=20),
            status="scheduled",
            risk_score=0.62,
            risk_level="MEDIUM",
        ),
        Appointment(
            patient_id=patients[1].patient_id,
            doctor_id="DR-102",
            appointment_date=today + datetime.timedelta(days=1),
            appointment_time=datetime.time(11, 0),
            booking_date=today - datetime.timedelta(days=3),
            status="scheduled",
            risk_score=0.18,
            risk_level="LOW",
        ),
        Appointment(
            patient_id=patients[2].patient_id,
            doctor_id="DR-101",
            appointment_date=today,
            appointment_time=datetime.time(10, 0),
            booking_date=today - datetime.timedelta(days=35),
            status="cancelled",
            risk_score=0.81,
            risk_level="HIGH",
        ),
        Appointment(
            patient_id=patients[3].patient_id,
            doctor_id="DR-103",
            appointment_date=today + datetime.timedelta(days=3),
            appointment_time=datetime.time(15, 0),
            booking_date=today - datetime.timedelta(days=1),
            status="scheduled",
            risk_score=0.25,
            risk_level="LOW",
        ),
        Appointment(
            patient_id=patients[5].patient_id,
            doctor_id="DR-102",
            appointment_date=today + datetime.timedelta(days=1),
            appointment_time=datetime.time(9, 0),
            booking_date=today - datetime.timedelta(days=14),
            status="scheduled",
            risk_score=0.55,
            risk_level="MEDIUM",
        ),
    ]
    db.add_all(appointments)

    waitlist_entries = [
        Waitlist(
            patient_id=patients[4].patient_id,
            preferred_doctor="DR-101",
            preferred_date=today - datetime.timedelta(days=1),
            arrival_time="09:30",
            priority=4,
        ),
        Waitlist(
            patient_id=patients[3].patient_id,
            preferred_doctor="DR-101",
            preferred_date=today,
            arrival_time="10:00",
            priority=2,
        ),
        Waitlist(
            patient_id=patients[1].patient_id,
            preferred_doctor="DR-102",
            preferred_date=today,
            arrival_time="11:15",
            priority=5,
        ),
    ]
    db.add_all(waitlist_entries)

    db.commit()
    print("[seed] Demo data seeded: patients, appointments, waitlist entries.")
