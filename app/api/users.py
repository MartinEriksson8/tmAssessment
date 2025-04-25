from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.user import UserCreate, UserUpdate, User
from app.models.user import User as UserModel
from app.dependencies import get_db
from typing import List

router = APIRouter()

@router.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    Args:
        user (UserCreate): User data including email, username, and password
        
    Returns:
        User: The created user object
        
    Raises:
        HTTPException: 400 if email or username is already registered
    """
    # Check if email exists
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # If unique, create new user
    db_user = UserModel(
        email=user.email,
        username=user.username,
    )
    db_user.set_password(user.password)  # This will hash the password
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/users/", response_model=List[User])
async def read_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.
    
    Returns:
        List[User]: List of all users in the system
    """
    # Get all users from db
    users = db.query(UserModel).all()
    return users

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    
    Args:
        user_id (int): The ID of the user to retrieve
        
    Returns:
        User: The requested user object
        
    Raises:
        HTTPException: 404 if user is not found
    """
    # Get single user by id
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user.
    
    Args:
        user_id (int): The ID of the user to update
        user_update (UserUpdate): The updated user data
        
    Returns:
        User: The updated user object
        
    Raises:
        HTTPException: 404 if user is not found
        HTTPException: 400 if email or username is already taken by another user
        HTTPException: 400 if there's a conflict with existing data
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if new email or username already exists
    if user_update.email:
        existing_user = db.query(UserModel).filter(
            UserModel.email == user_update.email,
            UserModel.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered by another user")
    
    if user_update.username:
        existing_user = db.query(UserModel).filter(
            UserModel.username == user_update.username,
            UserModel.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken by another user")
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Handle password update separately to ensure it's hashed
    if "password" in update_data:
        db_user.set_password(update_data.pop("password"))
    
    # Update other fields
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not update user due to a conflict with existing data"
        )

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.
    
    Args:
        user_id (int): The ID of the user to delete
        
    Raises:
        HTTPException: 404 if user is not found
    """
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return None
