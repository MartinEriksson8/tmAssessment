from pydantic import BaseModel, HttpUrl
from typing import Optional

class BookmarkBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: HttpUrl

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None

class Bookmark(BookmarkBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
