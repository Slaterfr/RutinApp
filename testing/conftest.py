import os
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

# Create an in-memory SQLite engine with StaticPool
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Patch db.database before importing main and services
from db import database

class TestSessionProxy:
    def __init__(self, engine):
        self.engine = engine
        self._session = Session(self.engine, expire_on_commit=False)

    def __enter__(self):
        if not self._session.is_active:
            self._session = Session(self.engine, expire_on_commit=False)
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                self._session.commit()
            except Exception:
                self._session.rollback()
                raise
        else:
            self._session.rollback()

    def reset(self):
        if self._session:
            try:
                self._session.close()
            except Exception:
                pass
        self._session = Session(self.engine, expire_on_commit=False)

    def __getattr__(self, name):
        if not self._session.is_active:
            self._session = Session(self.engine, expire_on_commit=False)
        return getattr(self._session, name)

database.engine = test_engine
database.session = TestSessionProxy(test_engine)

from models import models
SQLModel.metadata.create_all(test_engine)

from main import app
from dependencys import utils, oauth2

@pytest.fixture(autouse=True)
def reset_database():
    """Drop and recreate all tables for each test to guarantee complete test isolation."""
    database.session.reset()
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield
    database.session.reset()
    SQLModel.metadata.drop_all(test_engine)

@pytest.fixture
def db_session():
    """Provide a direct session for test fixtures and assertions."""
    with Session(test_engine) as session:
        yield session

@pytest.fixture
def client():
    """FastAPI TestClient instance."""
    return TestClient(app)

@pytest.fixture
def user_a(db_session):
    """Test User A."""
    user = models.User(
        email="user_a@example.com",
        username="user_a",
        password=utils.hash("Password123!"),
        biography="I am user A"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def user_b(db_session):
    """Test User B."""
    user = models.User(
        email="user_b@example.com",
        username="user_b",
        password=utils.hash("Password456!"),
        biography="I am user B"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_headers_a(user_a):
    """Authorization header with valid JWT for User A."""
    token = oauth2.create_token(data={"user_id": user_a.id})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_b(user_b):
    """Authorization header with valid JWT for User B."""
    token = oauth2.create_token(data={"user_id": user_b.id})
    return {"Authorization": f"Bearer {token}"}
