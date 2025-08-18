from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Dict, List


class RelationshipTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Unique relationship type name")
    display_name: str = Field(..., min_length=1, max_length=100, description="Human-readable display name")
    description: Optional[str] = Field(None, description="Detailed description of the relationship")
    sort_order: int = Field(default=0, description="Display order for sorting")
    is_reciprocal: bool = Field(default=False, description="Whether the relationship is reciprocal (like spouse/sibling)")
    generation_offset: int = Field(default=0, description="Generation offset (-1 for parent, +1 for child, 0 for same generation)")
    calculation_rules: Optional[Dict] = Field(None, description="JSON rules for relationship calculations")

    @validator('name')
    def validate_name(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Name can only contain letters, numbers, underscores, and hyphens')
        return v.lower().strip()

    @validator('display_name')
    def validate_display_name(cls, v):
        return v.strip()

    @validator('generation_offset')
    def validate_generation_offset(cls, v):
        if v < -3 or v > 3:
            raise ValueError('Generation offset must be between -3 and 3')
        return v


class RelationshipTypeCreate(RelationshipTypeBase):
    pass


class RelationshipTypeUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None)
    is_active: Optional[bool] = Field(None)
    sort_order: Optional[int] = Field(None)
    is_reciprocal: Optional[bool] = Field(None)
    generation_offset: Optional[int] = Field(None)
    calculation_rules: Optional[Dict] = Field(None)

    @validator('display_name')
    def validate_display_name(cls, v):
        return v.strip() if v else v

    @validator('generation_offset')
    def validate_generation_offset(cls, v):
        if v is not None and (v < -3 or v > 3):
            raise ValueError('Generation offset must be between -3 and 3')
        return v


class RelationshipTypeResponse(RelationshipTypeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RelationshipTypeListResponse(BaseModel):
    id: int
    name: str
    display_name: str
    description: Optional[str]
    is_active: bool
    sort_order: int
    is_reciprocal: bool
    generation_offset: int

    class Config:
        from_attributes = True


class RelationshipOptionResponse(BaseModel):
    """Simple response for dropdown/selection options"""
    name: str = Field(..., description="Relationship type name (internal identifier)")
    display_name: str = Field(..., description="Human-readable display name")
    description: Optional[str] = Field(None, description="Brief description for tooltips")
    is_reciprocal: bool = Field(..., description="Whether relationship is reciprocal")

    class Config:
        from_attributes = True


class RelationshipCalculationPreview(BaseModel):
    """Preview of relationships that will be created when invitation is accepted"""
    member_id: int
    member_name: str
    current_relationship: str
    derived_relationship: str
    relationship_display: str


class RelationshipValidationResponse(BaseModel):
    """Response for relationship validation"""
    is_valid: bool
    error_message: Optional[str] = None
    suggestions: Optional[List[str]] = None