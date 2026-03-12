"""
Pytest configuration and shared fixtures for Nexus Sports tests.
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./data/test_nexus_sports.db"

# Override settings before importing the app
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["ENVIRONMENT"] = "test"
os.environ["LOG_LEVEL"] = "WARNING"

from backend.core.database import Base, get_db
from backend.main import app


# Create test engine
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables once for the entire test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Clean up test db file
    db_path = TEST_DATABASE_URL.replace("sqlite:///", "")
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def db():
    """Provide a clean database session per test."""
    db = TestSession()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def client():
    """Provide a FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def sample_fit_path():
    """Return path to a real FIT file in the data directory for integration tests."""
    # Use one of the existing test files
    fit_files = [
        "data/跑步20260311233629.fit",
        "data/跑步机20260310191805.fit",
        "data/龙岩市_登山20230408120415.fit",
        "data/三组动作9分钟20231122210840.fit",
    ]
    for path in fit_files:
        if os.path.exists(path):
            return path
    pytest.skip("No FIT test files available in data/")


@pytest.fixture
def sample_gpx_path():
    """Return path to a real GPX file in the data directory."""
    gpx_path = "data/北京市_骑行20201219154819.gpx"
    if os.path.exists(gpx_path):
        return gpx_path
    pytest.skip("No GPX test files available in data/")
