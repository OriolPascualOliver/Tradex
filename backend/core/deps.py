from typing import Generator

from sqlalchemy.orm import Session

from .database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for use in request handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
