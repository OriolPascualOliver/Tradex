import os
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure project root is in the import path
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Use an in-memory database for tests
os.environ["DATABASE_URL"] = "sqlite://"

from backend.core.database import Base
import backend.core.database as database
from httpx import Client, ASGITransport
from main import app

# Create an in-memory SQLite engine for testing
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def override_session_local():
    """Override the application's database session with an in-memory DB."""
    database.SessionLocal = TestingSessionLocal
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    transport = ASGITransport(app=app)
    with Client(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
