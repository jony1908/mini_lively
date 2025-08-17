from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .base import Base


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=True)
    
    # Enhanced profile fields
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    
    # Relationships
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent = relationship("User", back_populates="children")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True)

    @property
    def age(self) -> int:
        """Calculate and return the child's current age in years."""
        today = date.today()
        birth_date = self.date_of_birth
        
        # Calculate age by comparing year, month, and day
        age = today.year - birth_date.year
        
        # Check if birthday hasn't occurred this year yet
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age

    def __repr__(self):
        return f"<Child(id={self.id}, name='{self.first_name} {self.last_name}', age={self.age}, parent_id={self.parent_id})>"