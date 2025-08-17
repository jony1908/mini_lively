from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List


class ChildBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Child's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Child's last name")
    date_of_birth: date = Field(..., description="Child's date of birth")
    gender: Optional[str] = Field(None, max_length=20, description="Child's gender (optional)")
    interests: Optional[List[str]] = Field(None, description="Child's interests and hobbies as a list")
    skills: Optional[List[str]] = Field(None, description="Child's current skills and abilities as a list")
    avatar_url: Optional[str] = Field(None, description="URL to child's avatar image")

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v is not None and v.strip() == '':
            return None
        return v
    
    @validator('interests')
    def validate_interests(cls, v):
        if v is not None:
            # Remove empty strings and limit list size
            v = [interest.strip() for interest in v if interest.strip()]
            if len(v) > 20:  # Maximum 20 interests
                raise ValueError('Maximum 20 interests allowed')
        return v if v else None
    
    @validator('skills')
    def validate_skills(cls, v):
        if v is not None:
            # Remove empty strings and limit list size
            v = [skill.strip() for skill in v if skill.strip()]
            if len(v) > 15:  # Maximum 15 skills
                raise ValueError('Maximum 15 skills allowed')
        return v if v else None


class ChildCreate(ChildBase):
    pass  # parent_id will be automatically set from JWT token


class ChildUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, max_length=20)
    interests: Optional[List[str]] = Field(None, description="Child's interests and hobbies as a list")
    skills: Optional[List[str]] = Field(None, description="Child's current skills and abilities as a list")
    avatar_url: Optional[str] = Field(None, description="URL to child's avatar image")
    is_active: Optional[bool] = Field(None)

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v is not None and v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v


class ChildResponse(ChildBase):
    id: int
    parent_id: int
    age: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ChildListResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    age: int
    gender: Optional[str]
    avatar_url: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class ChildOptionsResponse(BaseModel):
    """Predefined options for child interests and skills"""
    interests: List[str] = Field(..., description="List of predefined interest options")
    skills: List[str] = Field(..., description="List of predefined skill options")
    
    class Config:
        schema_extra = {
            "example": {
                "interests": ["Sports", "Music", "Art", "Science", "Reading", "Gaming"],
                "skills": ["Swimming", "Piano", "Drawing", "Cycling", "Soccer", "Basketball"]
            }
        }