import pytest
from sqlalchemy.orm import Session
from app.models.bookmark import Bookmark
from app.models.user import User
from app.auth.security import get_password_hash, create_access_token

pytestmark = pytest.mark.bookmarks

@pytest.fixture
def test_user(db: Session):
    """Create a test user for bookmark tests"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_bookmark(db: Session, test_user):
    """Create a test bookmark"""
    bookmark = Bookmark(
        title="Test Bookmark",
        description="A test bookmark",
        url="https://example.com/",
        user_id=test_user.id
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark

@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for test requests"""
    token = create_access_token(data={"sub": test_user.username})
    return {"Authorization": f"Bearer {token}"}

def test_create_bookmark(client, db: Session, test_user, auth_headers):
    """Test creating a bookmark"""
    bookmark_data = {
        "title": "New Bookmark",
        "description": "A new bookmark",
        "url": "https://example.com/new"
    }
    response = client.post("/bookmarks/", json=bookmark_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == bookmark_data["title"]
    assert data["description"] == bookmark_data["description"]
    assert data["url"] == bookmark_data["url"]
    assert data["user_id"] == test_user.id

def test_get_bookmark(client, test_bookmark, auth_headers):
    """Test getting a bookmark"""
    response = client.get(f"/bookmarks/{test_bookmark.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_bookmark.id
    assert data["title"] == test_bookmark.title
    assert data["description"] == test_bookmark.description
    assert data["url"] == test_bookmark.url

def test_get_nonexistent_bookmark(client, auth_headers):
    """Test getting a non-existent bookmark"""
    response = client.get("/bookmarks/999999", headers=auth_headers)
    assert response.status_code == 404

def test_update_bookmark(client, test_bookmark, auth_headers):
    """Test updating a bookmark"""
    update_data = {
        "title": "Updated Bookmark",
        "description": "An updated bookmark",
        "url": "https://example.com/updated"
    }
    response = client.put(f"/bookmarks/{test_bookmark.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["url"] == update_data["url"]

def test_delete_bookmark(client, db: Session, test_bookmark, auth_headers):
    """Test deleting a bookmark"""
    response = client.delete(f"/bookmarks/{test_bookmark.id}", headers=auth_headers)
    assert response.status_code == 204
    assert response.content == b""
    # Verify the bookmark was actually deleted
    deleted_bookmark = db.query(Bookmark).filter(Bookmark.id == test_bookmark.id).first()
    assert deleted_bookmark is None

def test_delete_nonexistent_bookmark(client, auth_headers):
    """Test deleting a non-existent bookmark"""
    response = client.delete("/bookmarks/999999", headers=auth_headers)
    assert response.status_code == 404

def test_unauthorized_access(client, test_bookmark):
    """Test accessing bookmark endpoints without authentication"""
    # Try to create a bookmark without auth
    bookmark_data = {
        "title": "New Bookmark",
        "description": "A new bookmark",
        "url": "https://example.com/new"
    }
    response = client.post("/bookmarks/", json=bookmark_data)
    assert response.status_code == 401

    # Try to get a bookmark without auth
    response = client.get(f"/bookmarks/{test_bookmark.id}")
    assert response.status_code == 401

    # Try to update a bookmark without auth
    update_data = {"title": "Updated Bookmark"}
    response = client.put(f"/bookmarks/{test_bookmark.id}", json=update_data)
    assert response.status_code == 401

    # Try to delete a bookmark without auth
    response = client.delete(f"/bookmarks/{test_bookmark.id}")
    assert response.status_code == 401
