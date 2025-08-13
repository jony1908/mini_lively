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

@pytest.fixture(scope="function")
def create_test_user(setup_database):
    """Create a test user for post tests."""
    user_data = {
        "username": "testauthor",
        "email": "author@example.com",
        "hashed_password": "hashedpassword123",
        "is_active": True
    }
    response = client.post("/api/users/", json=user_data)
    return response.json()

client = TestClient(app)

def test_create_post(create_test_user):
    """Test creating a new post."""
    user = create_test_user
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content.",
        "author_id": user["id"],
        "is_published": True
    }
    response = client.post("/api/posts/", json=post_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post content."
    assert data["author_id"] == user["id"]
    assert "id" in data

def test_read_posts(create_test_user):
    """Test reading posts list."""
    response = client.get("/api/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_post_not_found(create_test_user):
    """Test reading non-existent post."""
    response = client.get("/api/posts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"

def test_create_post_invalid_author(setup_database):
    """Test creating post with non-existent author."""
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content.",
        "author_id": 999,
        "is_published": True
    }
    response = client.post("/api/posts/", json=post_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"

def test_read_user_posts(create_test_user):
    """Test reading posts by specific user."""
    user = create_test_user
    
    post_data = {
        "title": "User's First Post",
        "content": "Content of the first post.",
        "author_id": user["id"],
        "is_published": True
    }
    client.post("/api/posts/", json=post_data)
    
    response = client.get(f"/api/posts/user/{user['id']}")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    if posts:
        assert posts[0]["author_id"] == user["id"]

def test_read_posts_for_nonexistent_user(setup_database):
    """Test reading posts for non-existent user."""
    response = client.get("/api/posts/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"