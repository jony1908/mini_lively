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
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member_relationships = relationship("UserToMember", foreign_keys="UserToMember.user_id", back_populates="user", cascade="all, delete-orphan")
    sent_invitations = relationship("UserInvitation", foreign_keys="UserInvitation.inviter_user_id", back_populates="inviter", cascade="all, delete-orphan")
    received_invitations = relationship("UserInvitation", foreign_keys="UserInvitation.invitee_user_id", back_populates="invitee")

    def __repr__(self):
        name_part = f"{self.first_name or ''} {self.last_name or ''}".strip()
        name_display = f"'{name_part}'" if name_part else "No Name"
        
        status_parts = []
        if not self.is_active:
            status_parts.append("inactive")
        if not self.is_verified:
            status_parts.append("unverified")
        if self.oauth_provider:
            status_parts.append(f"oauth:{self.oauth_provider}")
        
        status_str = f" [{', '.join(status_parts)}]" if status_parts else ""
        
        return f"<User(#{self.id}: {name_display} <{self.email}>{status_str})>"
    
    def __str__(self):
        name_part = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return f"{name_part} ({self.email})" if name_part else self.email