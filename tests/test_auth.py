import pytest
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.security import get_password_hash, create_access_token
from app.auth.deps import get_current_user
from datetime import datetime, timedelta
import time
from fastapi import HTTPException
import asyncio

pytestmark = pytest.mark.auth

@pytest.fixture
def test_user(db: Session):
    """Create a test user for authentication tests"""
    user = User(
        email="authtest@example.com",
        username="authtestuser",
        hashed_password=get_password_hash("testpassword")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.mark.asyncio
async def test_token_creation_and_verification(test_user, db: Session):
    """Test JWT token creation and verification"""
    # Create a token
    token = create_access_token(data={"sub": test_user.username})
    
    # Verify the token by getting the current user
    user = await get_current_user(token, db)
    assert user is not None
    assert user.username == test_user.username

@pytest.mark.asyncio
async def test_invalid_token(db: Session):
    """Test invalid token verification"""
    # Test with invalid token
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid.token.here", db)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_expired_token(test_user, db: Session):
    """Test expired token verification"""
    # Create a token that expired 1 second ago
    token = create_access_token(data={"sub": test_user.username}, expires_delta=timedelta(seconds=-1))
    
    # Verify token is expired
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token, db)
    assert exc_info.value.status_code == 401

@pytest.mark.asyncio
async def test_token_with_wrong_secret(test_user, db: Session):
    """Test token verification with wrong secret"""
    # Create a token with correct secret
    token = create_access_token(data={"sub": test_user.username})
    
    # Modify the token to simulate wrong secret
    parts = token.split('.')
    parts[2] = 'wrongsignature'
    wrong_token = '.'.join(parts)
    
    # Verify token is invalid
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(wrong_token, db)
    assert exc_info.value.status_code == 401
