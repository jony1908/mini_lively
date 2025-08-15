from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional


class ChildBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Child's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Child's last name")
    date_of_birth: date = Field(..., description="Child's date of birth")
    gender: Optional[str] = Field(None, max_length=20, description="Child's gender (optional)")
    interests: Optional[str] = Field(None, max_length=1000, description="Child's interests and hobbies")
    skills: Optional[str] = Field(None, max_length=1000, description="Child's current skills and abilities")

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


class ChildCreate(ChildBase):
    parent_id: int = Field(..., description="ID of the parent/guardian")


class ChildUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, max_length=20)
    interests: Optional[str] = Field(None, max_length=1000)
    skills: Optional[str] = Field(None, max_length=1000)
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
    is_active: bool

    class Config:
        from_attributes = True