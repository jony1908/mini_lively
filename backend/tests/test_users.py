import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_user(setup_database):
    """Test creating a new user."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": "hashedpassword123",
        "is_active": True
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_users(setup_database):
    """Test reading users list."""
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_user_not_found(setup_database):
    """Test reading non-existent user."""
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_duplicate_email(setup_database):
    """Test creating user with duplicate email."""
    user_data = {
        "username": "testuser1",
        "email": "test@example.com",
        "hashed_password": "hashedpassword123"
    }
    client.post("/api/users/", json=user_data)
    
    duplicate_user_data = {
        "username": "testuser2",
        "email": "test@example.com",
        "hashed_password": "hashedpassword456"
    }
    response = client.post("/api/users/", json=duplicate_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_duplicate_username(setup_database):
    """Test creating user with duplicate username."""
    user_data = {
        "username": "testuser",
        "email": "test1@example.com",
        "hashed_password": "hashedpassword123"
    }
    client.post("/api/users/", json=user_data)
    
    duplicate_user_data = {
        "username": "testuser",
        "email": "test2@example.com",
        "hashed_password": "hashedpassword456"
    }
    response = client.post("/api/users/", json=duplicate_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"