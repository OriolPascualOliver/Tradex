import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

TEST_DB = "test.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB}")

from backend.core.database import Base
import backend.core.database as database
from backend.api.models import user, task  # ensure models imported

# Create an in-memory SQLite engine
engine = create_engine(
    f"sqlite:///{TEST_DB}",
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def override_session_local():
    database.SessionLocal = TestingSessionLocal
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
