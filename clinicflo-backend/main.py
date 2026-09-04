"""
ClinicFlo backend - FastAPI entrypoint.

Hackathon prototype: no-show risk prediction + waitlist slot recovery for
hospital OPDs. Run with:

    uvicorn main:app --reload --port 8000

Swagger docs: http://localhost:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from seed import seed_if_empty

# Import all models so they register with Base.metadata before create_all.
from models import patient, appointment, waitlist, prediction  # noqa: F401

from routes import auth, patients, appointments, predictions, waitlist as waitlist_routes

app = FastAPI(
    title="ClinicFlo API",
    description=(
        "No-show prediction + waitlist slot recovery for hospital OPDs. "
        "Hackathon prototype -- not production-grade."
    ),
    version="0.1.0",
)

# Allow the React frontend (running on a different port, e.g. 5173/3000) to
# call this API during local development. Loosened for the hackathon demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(predictions.router)
app.include_router(waitlist_routes.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "ClinicFlo API", "docs": "/docs"}
