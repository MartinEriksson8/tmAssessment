import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.user import User
from app.models.bookmark import Bookmark
from app.auth.security import get_password_hash

pytestmark = pytest.mark.db

def test_database_connection(db: Session):
    """Test basic database connection"""
    # Try to execute a simple query
    result = db.execute(text("SELECT 1"))
    assert result.scalar() == 1

def test_cascade_delete(db: Session):
    """Test that bookmarks are deleted when user is deleted"""
    # Create a user
    user = User(
        email="cascade@example.com",
        username="cascadeuser",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    
    # Create a bookmark for the user
    bookmark = Bookmark(
        title="Cascade Bookmark",
        url="https://example.com",
        description="Test Cascade",
        user_id=user.id
    )
    db.add(bookmark)
    db.commit()
    
    # Delete the user
    db.delete(user)
    db.commit()
    
    # Verify bookmark was also deleted
    saved_bookmark = db.query(Bookmark).filter(Bookmark.title == "Cascade Bookmark").first()
    assert saved_bookmark is None 