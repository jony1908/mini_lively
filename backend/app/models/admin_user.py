from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .base import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Admin specific fields
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        status_parts = []
        if self.is_superuser:
            status_parts.append("superuser")
        if not self.is_active:
            status_parts.append("inactive")
        
        status_str = f" [{', '.join(status_parts)}]" if status_parts else ""
        
        return f"<AdminUser(#{self.id}: '{self.username}'{status_str})>"
    
    def __str__(self):
        status = ""
        if self.is_superuser:
            status += " (superuser)"
        if not self.is_active:
            status += " (inactive)"
        return f"{self.username}{status}"