from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .base import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=True)
    
    # Enhanced profile fields
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user_relationships = relationship("UserToMember", back_populates="member", cascade="all, delete-orphan")

    @property
    def age(self) -> int:
        """Calculate and return the member's current age in years."""
        today = date.today()
        birth_date = self.date_of_birth
        
        # Calculate age by comparing year, month, and day
        age = today.year - birth_date.year
        
        # Check if birthday hasn't occurred this year yet
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age

    def __repr__(self):
        name = f"{self.first_name} {self.last_name}"
        
        details = []
        details.append(f"age {self.age}")
        if self.gender:
            details.append(self.gender)
        if not self.is_active:
            details.append("inactive")
        if self.avatar_url:
            details.append("has_avatar")
        
        interests_count = len(self.interests) if self.interests else 0
        skills_count = len(self.skills) if self.skills else 0
        if interests_count or skills_count:
            details.append(f"{interests_count}i/{skills_count}s")
        
        details_str = f" [{', '.join(details)}]" if details else ""
        
        return f"<Member(#{self.id}: '{name}'{details_str})>"
    
    def __str__(self):
        status = " (inactive)" if not self.is_active else ""
        return f"{self.first_name} {self.last_name}, age {self.age}{status}"