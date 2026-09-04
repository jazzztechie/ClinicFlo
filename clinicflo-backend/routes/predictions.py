from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.appointment import Appointment
from models.prediction import Prediction
from schemas import PredictRequest, PredictResponse
from services import prediction as prediction_service
from services import decision_engine

router = APIRouter(tags=["predictions"])


@router.post("/predict", response_model=PredictResponse)
def predict_no_show(payload: PredictRequest, db: Session = Depends(get_db)):
    """
    Core prediction endpoint.

    Flow: services/prediction.py (ML model wrapper) -> raw probability
          -> services/decision_engine.py -> risk tier + recommended action

    If `appointment_id` is supplied, the matching Appointment row's
    risk_score/risk_level are updated and a Prediction record is logged.
    """
    appointment = None
    if payload.appointment_id is not None:
        appointment = (
            db.query(Appointment)
            .filter(Appointment.appointment_id == payload.appointment_id)
            .first()
        )
        if appointment is None:
            raise HTTPException(
                status_code=404,
                detail=f"Appointment {payload.appointment_id} not found",
            )

    patient_data = payload.model_dump(exclude={"appointment_id"})
    ml_result = prediction_service.predict(patient_data)
    decision = decision_engine.evaluate(ml_result["probability"])

    response = PredictResponse(
        probability=ml_result["probability"],
        risk_level=decision["risk_level"],
        reasons=ml_result["reasons"],
        recommended_action=decision["recommended_action"],
    )

    # Persist the prediction, and update the appointment if one was linked.
    record = Prediction(
        appointment_id=payload.appointment_id,
        probability=response.probability,
        risk_level=response.risk_level,
    )
    db.add(record)

    if appointment is not None:
        appointment.risk_score = response.probability
        appointment.risk_level = response.risk_level

    db.commit()

    return response
