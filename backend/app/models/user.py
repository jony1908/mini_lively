from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)  # Nullable for OAuth users
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)  # 'google', 'apple', or None for email/password
    oauth_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        name_part = f"{self.first_name or ''} {self.last_name or ''}".strip() or "No Name"
        return f"<User(id={self.id}, email='{self.email}', name='{name_part}')>"
    
    def __str__(self):
        name_part = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return f"{name_part} ({self.email})" if name_part else self.email