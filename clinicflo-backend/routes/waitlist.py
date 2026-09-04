from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.waitlist import Waitlist
from models.patient import Patient
from models.appointment import Appointment
from schemas import WaitlistCreate, WaitlistOut, MatchSlotRequest, MatchSlotResponse
from services import waitlist_matching

router = APIRouter(tags=["waitlist"])


@router.get("/waitlist", response_model=list[WaitlistOut])
def list_waitlist(db: Session = Depends(get_db)):
    return db.query(Waitlist).order_by(Waitlist.priority.desc(), Waitlist.preferred_date).all()


@router.post("/waitlist", response_model=WaitlistOut, status_code=201)
def add_to_waitlist(payload: WaitlistCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == payload.patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail=f"Patient {payload.patient_id} not found")

    entry = Waitlist(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/waitlist/{waitlist_id}", status_code=204)
def remove_from_waitlist(waitlist_id: int, db: Session = Depends(get_db)):
    entry = db.query(Waitlist).filter(Waitlist.waitlist_id == waitlist_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Waitlist entry {waitlist_id} not found")
    db.delete(entry)
    db.commit()
    return None


@router.post("/match-slot", response_model=MatchSlotResponse)
def match_slot(payload: MatchSlotRequest, db: Session = Depends(get_db)):
    """
    Given a freed-up appointment slot (slot_id = appointment_id), find the
    best-matching waitlisted patient using a deterministic priority score
    (NOT ML -- see services/waitlist_matching.py).
    """
    slot = db.query(Appointment).filter(Appointment.appointment_id == payload.slot_id).first()
    if slot is None:
        raise HTTPException(status_code=404, detail=f"Slot (appointment) {payload.slot_id} not found")

    best_entry, reason, runner_up_count = waitlist_matching.find_best_match(db, slot)

    return MatchSlotResponse(
        recommended_patient=best_entry,
        reason=reason,
        runner_up_count=runner_up_count,
    )
