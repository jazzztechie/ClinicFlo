# ClinicFlo Backend

No-show prediction + waitlist slot recovery for hospital OPDs.
Hackathon prototype — prioritizes a working end-to-end demo over production robustness.

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Swagger docs: http://localhost:8000/docs
The SQLite DB (`clinicflo.db`) and demo seed data are created automatically on first startup.

## Demo login

```
POST /login
{ "username": "reception", "password": "clinicflo123" }
```

## Phase 1 vs Phase 2 (ML model)

- **Phase 1 (now):** `/predict` works immediately using a transparent, hand-tuned
  heuristic in `services/prediction.py` (`_dummy_predict_proba`). No `.pkl` file needed.
- **Phase 2 (once the ML team delivers a model):** drop the trained model at
  `model/clinicflo_model.pkl`. It must expose a scikit-learn-style
  `predict_proba(X)` method, with `X` columns in this order:
  `age, gender_code (0=M/1=F/2=Other), scholarship, hypertension, diabetes, sms_received, lead_time`.
  `services/prediction.py` auto-detects the file on next server startup and
  switches to it — no route or schema changes required.
- Want to test the "real model" code path today? Run
  `python model/train_placeholder_model.py` to generate a placeholder `.pkl`.

## Architecture

```
routes/          -> HTTP layer only, no ML/business logic
services/prediction.py       -> ML model wrapper (probability + reasons only)
services/decision_engine.py  -> probability -> risk tier -> action (no ML)
services/waitlist_matching.py -> deterministic (non-ML) slot-matching score
models/          -> SQLAlchemy ORM models
schemas.py       -> Pydantic request/response validation
seed.py          -> demo data
```

## Key endpoints

| Method | Path              | Purpose                                   |
|--------|-------------------|--------------------------------------------|
| POST   | /login             | Demo-only auth                            |
| GET    | /patients          | List patients                             |
| POST   | /patients          | Create patient                            |
| GET    | /appointments      | List appointments (poll for updates)      |
| POST   | /appointments      | Create appointment                        |
| PUT    | /appointments/{id} | Update appointment (status, risk, etc.)   |
| POST   | /predict           | Core no-show risk prediction              |
| GET    | /waitlist          | List waitlist                             |
| POST   | /waitlist          | Add to waitlist                           |
| DELETE | /waitlist/{id}     | Remove from waitlist                      |
| POST   | /match-slot        | Recommend best waitlist patient for a slot|

## Notes

- Risk thresholds (`LOW < 0.40 <= MEDIUM < 0.70 <= HIGH`) are configurable
  prototype values in `services/decision_engine.py`, not validated clinical cutoffs.
- "Reasons" returned by `/predict` describe predictive/correlational factors,
  not causal claims.
- No real SMS/WhatsApp integration — reminders are simulated via the
  `recommended_action` string only.
- No WebSockets — the frontend should poll `GET /appointments`.
