"""
ClinicFlo - Database setup
SQLite for the hackathon prototype. Swap SQLALCHEMY_DATABASE_URL for a
PostgreSQL DSN later (e.g. "postgresql://user:pass@host/db") with no other
code changes required.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./clinicflo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Needed only for SQLite: allows the connection to be used across
    # the threads FastAPI's threadpool may dispatch a request to.
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
