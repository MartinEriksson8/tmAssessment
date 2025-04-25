from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models.bookmark import Bookmark as BookmarkModel
from app.schemas.bookmark import BookmarkCreate, Bookmark, BookmarkUpdate
from app.auth.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Bookmark)
async def create_bookmark(
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new bookmark for the current user.
    
    Args:
        bookmark (BookmarkCreate): Bookmark data including title, description, and URL
        
    Returns:
        Bookmark: The created bookmark object
        
    Raises:
        HTTPException: 401 if user is not authenticated
    """
    bookmark_data = bookmark.model_dump()
    db_bookmark = BookmarkModel(
        title=bookmark_data["title"],
        description=bookmark_data["description"],
        url=str(bookmark_data["url"]),
        user_id=current_user.id
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

@router.get("/", response_model=List[Bookmark])
async def list_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all bookmarks for the current user.
    
    Returns:
        List[Bookmark]: List of all bookmarks belonging to the current user
        
    Raises:
        HTTPException: 401 if user is not authenticated
    """
    return db.query(BookmarkModel).filter(BookmarkModel.user_id == current_user.id).all()

@router.get("/{bookmark_id}", response_model=Bookmark)
async def get_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific bookmark by ID.
    
    Args:
        bookmark_id (int): The ID of the bookmark to retrieve
        
    Returns:
        Bookmark: The requested bookmark object
        
    Raises:
        HTTPException: 404 if bookmark is not found
        HTTPException: 401 if user is not authenticated
    """
    bookmark = db.query(BookmarkModel).filter(
        BookmarkModel.id == bookmark_id,
        BookmarkModel.user_id == current_user.id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark

@router.put("/{bookmark_id}", response_model=Bookmark)
async def update_bookmark(
    bookmark_id: int,
    bookmark_update: BookmarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a bookmark.
    
    Args:
        bookmark_id (int): The ID of the bookmark to update
        bookmark_update (BookmarkUpdate): The updated bookmark data
        
    Returns:
        Bookmark: The updated bookmark object
        
    Raises:
        HTTPException: 404 if bookmark is not found
        HTTPException: 401 if user is not authenticated
    """
    db_bookmark = db.query(BookmarkModel).filter(
        BookmarkModel.id == bookmark_id,
        BookmarkModel.user_id == current_user.id
    ).first()
    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    update_data = bookmark_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "url" and value is not None:
            value = str(value)
        setattr(db_bookmark, field, value)
    
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

@router.delete("/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a bookmark.
    
    Args:
        bookmark_id (int): The ID of the bookmark to delete
        
    Returns:
        dict: A message confirming the deletion
        
    Raises:
        HTTPException: 404 if bookmark is not found
        HTTPException: 401 if user is not authenticated
    """
    bookmark = db.query(BookmarkModel).filter(
        BookmarkModel.id == bookmark_id,
        BookmarkModel.user_id == current_user.id
    ).first()
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Bookmark deleted successfully"}
