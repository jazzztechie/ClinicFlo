"""
ClinicFlo - Auth routes

DEMO-ONLY authentication. There is no real user store, hashing, or session
management -- this exists purely so the frontend has a /login call to hit.
Do NOT use this pattern in production.
"""
from fastapi import APIRouter, HTTPException

from schemas import LoginRequest, LoginResponse

router = APIRouter(tags=["auth"])

# Hardcoded demo credentials.
_DEMO_USERS = {
    "reception": "clinicflo123",
    "admin": "clinicflo123",
}


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    expected_password = _DEMO_USERS.get(payload.username)
    if expected_password is None or expected_password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Fake token -- fine for a hackathon demo, never do this for real auth.
    fake_token = f"demo-token-{payload.username}"
    return LoginResponse(access_token=fake_token, user=payload.username)
