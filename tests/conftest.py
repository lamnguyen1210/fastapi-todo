import os

# Set test env vars BEFORE importing any app modules.
# python-dotenv's load_dotenv() won't override these (override=False by default).
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base
from app.dependencies import get_db

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """
    Create all tables before each test, drop them after.
    This gives each test a clean, empty database.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """
    A TestClient that uses the test SQLite DB instead of the real PostgreSQL DB.

    JS analogy: this overrides the DB dependency — like mocking a module in Jest,
    except FastAPI's dependency injection makes it clean and explicit.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client):
    """
    A client with a pre-registered and logged-in user.
    Returns (client, token, user_data) so tests can make authenticated requests.
    """
    user_data = {"email": "test@example.com", "password": "testpassword123"}
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 201, register_response.text
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return client, token, user_data
