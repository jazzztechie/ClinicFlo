"""
ClinicFlo - Waitlist matching service

Deterministic (NOT ML) scoring used to recommend which waitlisted patient
should be offered a freed-up appointment slot.

priority_score = waiting_time_score + doctor_match + preferred_time_match + urgency

All four components are simple, explainable prototype heuristics.
"""
import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models.waitlist import Waitlist
from models.appointment import Appointment


def _waiting_time_score(entry: Waitlist) -> float:
    """
    Longer-waiting entries (i.e. those that joined the waitlist for an
    earlier preferred_date) score higher. We approximate "time spent
    waiting" using how far in the past the preferred_date is relative to
    today -- a patient whose preferred date already passed has been
    waiting longer / is more overdue.
    """
    today = datetime.date.today()
    days_overdue = (today - entry.preferred_date).days
    # Clamp and scale: 0 if not yet due, up to 10 points for being very overdue.
    return max(0.0, min(days_overdue, 20)) / 2.0


def _doctor_match_score(entry: Waitlist, slot_doctor_id: str) -> float:
    return 10.0 if entry.preferred_doctor == slot_doctor_id else 0.0


def _preferred_time_match_score(entry: Waitlist, slot_time: datetime.time) -> float:
    """Award points the closer the waitlist's preferred arrival_time is to the slot time."""
    try:
        pref_hour, pref_minute = (int(x) for x in entry.arrival_time.split(":")[:2])
    except (ValueError, AttributeError):
        return 0.0
    pref_minutes = pref_hour * 60 + pref_minute
    slot_minutes = slot_time.hour * 60 + slot_time.minute
    diff = abs(pref_minutes - slot_minutes)
    if diff <= 15:
        return 8.0
    if diff <= 60:
        return 4.0
    if diff <= 120:
        return 1.0
    return 0.0


def _urgency_score(entry: Waitlist) -> float:
    # priority is user-set 1 (low) - 5 (urgent); scale to 0-10.
    return entry.priority * 2.0


def score_entry(entry: Waitlist, slot: Appointment) -> float:
    return (
        _waiting_time_score(entry)
        + _doctor_match_score(entry, slot.doctor_id)
        + _preferred_time_match_score(entry, slot.appointment_time)
        + _urgency_score(entry)
    )


def _reason_for(entry: Waitlist, slot: Appointment, score: float) -> str:
    parts = []
    if entry.preferred_doctor == slot.doctor_id:
        parts.append(f"requested doctor {slot.doctor_id}")
    if _preferred_time_match_score(entry, slot.appointment_time) >= 4.0:
        parts.append(f"preferred time close to slot ({entry.arrival_time})")
    if entry.priority >= 4:
        parts.append(f"high urgency (priority {entry.priority})")
    days_overdue = (datetime.date.today() - entry.preferred_date).days
    if days_overdue > 0:
        parts.append(f"waiting since {entry.preferred_date.isoformat()} ({days_overdue}d overdue)")

    if not parts:
        parts.append("best available match on the waitlist")

    return f"Top match (score {score:.1f}): " + ", ".join(parts)


def find_best_match(db: Session, slot: Appointment) -> tuple[Optional[Waitlist], str, int]:
    """
    Returns (best_entry_or_None, reason, runner_up_count).
    """
    entries = db.query(Waitlist).all()
    if not entries:
        return None, "No patients currently on the waitlist.", 0

    scored = sorted(
        ((entry, score_entry(entry, slot)) for entry in entries),
        key=lambda pair: pair[1],
        reverse=True,
    )

    best_entry, best_score = scored[0]
    reason = _reason_for(best_entry, slot, best_score)
    runner_up_count = len(scored) - 1

    return best_entry, reason, runner_up_count
