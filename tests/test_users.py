import pytest
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.security import get_password_hash

pytestmark = pytest.mark.users

@pytest.fixture
def test_user(db: Session):
    """Create a test user for authentication tests"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.mark.auth
def test_create_user(client, db: Session):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword"
    }
    response = client.post("/users/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data

@pytest.mark.auth
def test_create_user_duplicate_email(client, db: Session, test_user):
    """Test user registration with duplicate email"""
    user_data = {
        "email": test_user.email,
        "username": "differentuser",
        "password": "password123"
    }
    response = client.post("/users/users/", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

@pytest.mark.auth
def test_create_user_duplicate_username(client, db: Session, test_user):
    """Test user registration with duplicate username"""
    user_data = {
        "email": "different@example.com",
        "username": test_user.username,
        "password": "password123"
    }
    response = client.post("/users/users/", json=user_data)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]

def test_get_user(client, db: Session, test_user):
    """Test getting user details"""
    response = client.get(f"/users/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username

def test_get_nonexistent_user(client):
    """Test getting details of a non-existent user"""
    response = client.get("/users/users/999999")
    assert response.status_code == 404

def test_update_user(client, db: Session, test_user):
    """Test updating user details"""
    update_data = {
        "username": "updatedusername",
        "email": "updated@example.com"
    }
    response = client.put(f"/users/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == update_data["username"]
    assert data["email"] == update_data["email"]

def test_update_user_password(client, db: Session, test_user):
    """Test updating user password"""
    update_data = {
        "password": "newpassword123"
    }
    response = client.put(f"/users/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    # Verify the password was actually changed
    db.refresh(test_user)
    assert test_user.verify_password("newpassword123")

def test_delete_user(client, db: Session, test_user):
    """Test deleting a user"""
    response = client.delete(f"/users/users/{test_user.id}")
    assert response.status_code == 204
    assert response.content == b""
    # Verify the user was actually deleted
    deleted_user = db.query(User).filter(User.id == test_user.id).first()
    assert deleted_user is None

def test_delete_nonexistent_user(client):
    """Test deleting a non-existent user"""
    response = client.delete("/users/users/999999")
    assert response.status_code == 404
