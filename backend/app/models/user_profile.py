from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    
    # Contact Information
    phone_number = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    
    # Location
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True, index=True)  # Index for fast regional searches
    country = Column(String, nullable=True)
    
    # Activity Preferences (stored as JSON strings)
    preferred_activity_types = Column(Text, nullable=True)  # JSON field for activity interests
    preferred_schedule = Column(Text, nullable=True)  # JSON field for availability preferences
    
    # Settings
    timezone = Column(String, nullable=True)
    notification_preferences = Column(Text, nullable=True)  # JSON field for communication preferences
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User", back_populates="profile")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id}, city='{self.city}', postal_code='{self.postal_code}')>"