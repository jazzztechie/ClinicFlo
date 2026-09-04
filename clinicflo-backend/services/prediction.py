"""
ClinicFlo - Prediction service

Wraps the no-show prediction model. This module is deliberately the ONLY
place that touches the ML model. It knows nothing about risk tiers or
recommended actions -- that's services/decision_engine.py's job. It only
outputs a probability (0-1) plus a list of contributing-feature "reasons".

Phase 1 (hackathon demo): no trained model exists yet, so we use a simple,
transparent heuristic ("dummy model") that produces plausible, input-sensitive
probabilities. This lets the /predict endpoint and the frontend integration
work end-to-end immediately.

Phase 2: once the ML team drops a trained model at model/clinicflo_model.pkl
(expected to expose a scikit-learn-style `.predict_proba(X)` method), this
module will automatically detect and use it instead of the heuristic -- no
route or schema changes required.

Expected pickled model contract:
    model.predict_proba(X) -> ndarray of shape (n_samples, 2)
    where column 1 is the probability of a no-show.
    X is a 2D array with columns in FEATURE_ORDER (see below).
"""
from __future__ import annotations

import os
from typing import Any

import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "clinicflo_model.pkl")

# Column order expected by the trained model. Keep this in sync with the
# ML team's training pipeline.
FEATURE_ORDER = [
    "age",
    "gender_code",   # 0=M, 1=F, 2=Other
    "scholarship",
    "hypertension",
    "diabetes",
    "sms_received",
    "lead_time",
]

_model: Any = None
_model_load_attempted = False


def _try_load_model():
    """Attempt to load a real trained model from disk. Cached after first call."""
    global _model, _model_load_attempted
    if _model_load_attempted:
        return _model
    _model_load_attempted = True

    if os.path.exists(MODEL_PATH):
        try:
            import joblib

            _model = joblib.load(MODEL_PATH)
            print(f"[prediction] Loaded trained model from {MODEL_PATH}")
        except Exception as exc:  # pragma: no cover - defensive, hackathon demo
            print(f"[prediction] Failed to load model at {MODEL_PATH}: {exc}")
            print("[prediction] Falling back to the built-in dummy model.")
            _model = None
    else:
        print(
            f"[prediction] No trained model found at {MODEL_PATH}. "
            "Using the built-in dummy heuristic model for now."
        )
    return _model


def _encode_gender(gender: str) -> int:
    return {"M": 0, "F": 1, "Other": 2}.get(gender, 2)


def _vectorize(patient_data: dict) -> np.ndarray:
    row = [
        patient_data["age"],
        _encode_gender(patient_data["gender"]),
        int(patient_data["scholarship"]),
        int(patient_data["hypertension"]),
        int(patient_data["diabetes"]),
        int(patient_data["sms_received"]),
        patient_data["lead_time"],
    ]
    return np.array([row], dtype=float)


def _dummy_predict_proba(patient_data: dict) -> float:
    """
    Transparent, hand-tuned heuristic standing in for a trained model.
    Purely additive weights on normalized-ish signals, clipped to [0.02, 0.98].
    This is NOT a validated clinical model -- prototype only.
    """
    score = 0.15  # base rate

    # Longer lead time -> more likely to forget / deprioritize the visit.
    lead_time = patient_data["lead_time"]
    if lead_time > 30:
        score += 0.30
    elif lead_time > 14:
        score += 0.20
    elif lead_time > 7:
        score += 0.10

    # Younger adults have historically higher no-show rates in OPD data;
    # very young (child, accompanied) and elderly (higher compliance) lower.
    age = patient_data["age"]
    if 18 <= age <= 35:
        score += 0.12
    elif age < 12 or age > 65:
        score -= 0.05

    # No SMS reminder sent yet -> higher risk.
    if not patient_data["sms_received"]:
        score += 0.15
    else:
        score -= 0.08

    # Scholarship / welfare enrollment historically correlates with
    # transport/cost-related access barriers in public OPD datasets.
    if patient_data["scholarship"]:
        score += 0.05

    # Chronic condition follow-ups tend to be *more* reliably attended.
    if patient_data["hypertension"]:
        score -= 0.04
    if patient_data["diabetes"]:
        score -= 0.04

    return float(np.clip(score, 0.02, 0.98))


def _generate_reasons(patient_data: dict, probability: float) -> list[str]:
    """
    Produce a short, human-readable list of the top predictive factors.
    These are correlational, not causal claims.
    """
    reasons = []

    lead_time = patient_data["lead_time"]
    if lead_time > 7:
        reasons.append(f"Long lead time ({lead_time} days between booking and visit)")

    age = patient_data["age"]
    if 18 <= age <= 35:
        reasons.append("Age group (18-35) with historically higher no-show rates")

    if not patient_data["sms_received"]:
        reasons.append("No reminder SMS sent yet")

    if patient_data["scholarship"]:
        reasons.append("Enrolled in welfare/scholarship program (associated with access barriers)")

    if patient_data["hypertension"] or patient_data["diabetes"]:
        reasons.append("Chronic condition follow-up (tends to correlate with better attendance)")

    if not reasons:
        reasons.append("No strong risk factors detected; baseline attendance rate assumed")

    return reasons


def predict(patient_data: dict) -> dict:
    """
    Main entry point. Accepts a dict with keys matching schemas.PredictRequest
    (minus appointment_id), returns:
        { "probability": float, "reasons": [str, ...] }

    Risk-tier / action mapping is intentionally NOT done here -- see
    services/decision_engine.py.
    """
    model = _try_load_model()

    if model is not None:
        X = _vectorize(patient_data)
        try:
            proba = float(model.predict_proba(X)[0][1])
        except Exception as exc:  # pragma: no cover - defensive, hackathon demo
            print(f"[prediction] Real model inference failed ({exc}); falling back to dummy model.")
            proba = _dummy_predict_proba(patient_data)
    else:
        proba = _dummy_predict_proba(patient_data)

    reasons = _generate_reasons(patient_data, proba)

    return {"probability": round(proba, 4), "reasons": reasons}
