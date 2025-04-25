from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.auth.security import get_password_hash, verify_password

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify a plain password against the user's hashed password.
        """
        return verify_password(plain_password, self.hashed_password)

    def set_password(self, password: str) -> None:
        """
        Set the user's password (hashes it before storing).
        """
        self.hashed_password = get_password_hash(password)
