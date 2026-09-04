"""
ClinicFlo - Decision engine

Converts a raw no-show probability (from services/prediction.py) into:
  1. a risk tier (LOW / MEDIUM / HIGH)
  2. a recommended operational action

Kept strictly separate from the prediction service: this module never
touches the ML model, and prediction.py never knows about risk tiers.
Thresholds below are configurable prototype values, not clinically
validated cutoffs.
"""
from typing import Literal

RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]

# Prototype thresholds -- tune freely, not validated cutoffs.
LOW_MEDIUM_THRESHOLD = 0.40
MEDIUM_HIGH_THRESHOLD = 0.70

ACTIONS: dict[RiskLevel, str] = {
    "LOW": "Send normal appointment reminder",
    "MEDIUM": "Send reminder and flag for front-desk monitoring",
    "HIGH": "Alert reception staff for proactive outreach / confirmation call",
}


def classify_risk(probability: float) -> RiskLevel:
    """Map a no-show probability to a risk tier."""
    if probability >= MEDIUM_HIGH_THRESHOLD:
        return "HIGH"
    if probability >= LOW_MEDIUM_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def recommend_action(risk_level: RiskLevel) -> str:
    """Map a risk tier to a recommended operational action."""
    return ACTIONS.get(risk_level, ACTIONS["LOW"])


def evaluate(probability: float) -> dict:
    """
    Convenience wrapper used by routes/predictions.py.
    Takes a raw probability, returns risk_level + recommended_action.
    """
    risk_level = classify_risk(probability)
    return {
        "risk_level": risk_level,
        "recommended_action": recommend_action(risk_level),
    }
