from pydantic import BaseModel, Field, validator, root_validator
from datetime import date, datetime
from typing import Optional, List
import json
import re


class MemberBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Member's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Member's last name")
    date_of_birth: date = Field(..., description="Member's date of birth")
    gender: Optional[str] = Field(None, max_length=20, description="Member's gender (optional)")
    relationship: Optional[str] = Field(None, max_length=50, description="Relationship to the user (optional)")
    interests: Optional[List[str]] = Field(None, description="Member's interests and hobbies as a list")
    skills: Optional[List[str]] = Field(None, description="Member's current skills and abilities as a list")
    avatar_url: Optional[str] = Field(None, description="URL to member's avatar image")

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
    
    @validator('interests', pre=True)
    def validate_interests(cls, v):
        if v is not None:
            # Handle PostgreSQL array format like {Acting,"Arts & Crafts"}
            if isinstance(v, str):
                if v.startswith('{') and v.endswith('}'):
                    # Parse PostgreSQL array format
                    array_content = v[1:-1]  # Remove { and }
                    if array_content:
                        # Split by comma but handle quoted strings
                        interests = []
                        current = ''
                        in_quotes = False
                        for char in array_content:
                            if char == '"' and (not current or current[-1] != '\\'):
                                in_quotes = not in_quotes
                            elif char == ',' and not in_quotes:
                                if current.strip():
                                    # Remove quotes if present
                                    interest = current.strip()
                                    if interest.startswith('"') and interest.endswith('"'):
                                        interest = interest[1:-1]
                                    interests.append(interest)
                                current = ''
                            else:
                                current += char
                        # Add the last item
                        if current.strip():
                            interest = current.strip()
                            if interest.startswith('"') and interest.endswith('"'):
                                interest = interest[1:-1]
                            interests.append(interest)
                        v = interests
                    else:
                        v = []
                else:
                    # Try to parse as JSON array
                    try:
                        v = json.loads(v) if v else []
                    except:
                        # If not JSON, treat as single item
                        v = [v]
            
            # Ensure it's a list
            if not isinstance(v, list):
                v = [v] if v else []
            
            # Remove empty strings and limit list size
            v = [interest.strip() for interest in v if isinstance(interest, str) and interest.strip()]
            if len(v) > 20:  # Maximum 20 interests
                raise ValueError('Maximum 20 interests allowed')
        return v if v else None
    
    @validator('skills', pre=True)
    def validate_skills(cls, v):
        if v is not None:
            # Handle PostgreSQL array format like {Swimming,"Piano Playing"}
            if isinstance(v, str):
                if v.startswith('{') and v.endswith('}'):
                    # Parse PostgreSQL array format
                    array_content = v[1:-1]  # Remove { and }
                    if array_content:
                        # Split by comma but handle quoted strings
                        skills = []
                        current = ''
                        in_quotes = False
                        for char in array_content:
                            if char == '"' and (not current or current[-1] != '\\'):
                                in_quotes = not in_quotes
                            elif char == ',' and not in_quotes:
                                if current.strip():
                                    # Remove quotes if present
                                    skill = current.strip()
                                    if skill.startswith('"') and skill.endswith('"'):
                                        skill = skill[1:-1]
                                    skills.append(skill)
                                current = ''
                            else:
                                current += char
                        # Add the last item
                        if current.strip():
                            skill = current.strip()
                            if skill.startswith('"') and skill.endswith('"'):
                                skill = skill[1:-1]
                            skills.append(skill)
                        v = skills
                    else:
                        v = []
                else:
                    # Try to parse as JSON array
                    try:
                        v = json.loads(v) if v else []
                    except:
                        # If not JSON, treat as single item
                        v = [v]
            
            # Ensure it's a list
            if not isinstance(v, list):
                v = [v] if v else []
            
            # Remove empty strings and limit list size
            v = [skill.strip() for skill in v if isinstance(skill, str) and skill.strip()]
            if len(v) > 15:  # Maximum 15 skills
                raise ValueError('Maximum 15 skills allowed')
        return v if v else None


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, max_length=20)
    relationship: Optional[str] = Field(None, max_length=50, description="Relationship to the user (optional)")
    interests: Optional[List[str]] = Field(None, description="Member's interests and hobbies as a list")
    skills: Optional[List[str]] = Field(None, description="Member's current skills and abilities as a list")
    avatar_url: Optional[str] = Field(None, description="URL to member's avatar image")
    is_active: Optional[bool] = Field(None)

    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        if v is not None and v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v


class MemberResponse(MemberBase):
    id: int
    age: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class MemberListResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date
    age: int
    gender: Optional[str]
    interests: Optional[List[str]]
    skills: Optional[List[str]]
    avatar_url: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class MemberOptionsResponse(BaseModel):
    """Predefined options for member interests and skills"""
    interests: List[str] = Field(..., description="List of predefined interest options")
    skills: List[str] = Field(..., description="List of predefined skill options")
    
    class Config:
        json_schema_extra = {
            "example": {
                "interests": ["Sports", "Music", "Art", "Science", "Reading", "Gaming"],
                "skills": ["Swimming", "Piano", "Drawing", "Cycling", "Soccer", "Basketball"]
            }
        }