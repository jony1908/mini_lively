from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any


class UserToMemberBase(BaseModel):
    user_id: int = Field(..., description="ID of the user in the relationship")
    member_id: int = Field(..., description="ID of the family member")
    relation: str = Field(..., max_length=50, description="Type of relationship (parent, child, spouse, etc.)")
    is_shareable: bool = Field(default=True, description="Whether this member can be shared with invited users")
    is_manager: bool = Field(default=True, description="Whether this user can edit/delete the member")
    relationship_notes: Optional[str] = Field(None, max_length=1000, description="Additional notes about the relationship")
    is_primary: bool = Field(default=False, description="Whether this is the primary relationship for this member")

    @validator('relation')
    def validate_relation(cls, v):
        return v.lower().strip()

    @validator('relationship_notes')
    def validate_notes(cls, v):
        if v:
            return v.strip()
        return v


class UserToMemberCreate(UserToMemberBase):
    pass


class UserToMemberUpdate(BaseModel):
    relation: Optional[str] = Field(None, max_length=50)
    is_shareable: Optional[bool] = Field(None)
    is_manager: Optional[bool] = Field(None)
    relationship_notes: Optional[str] = Field(None, max_length=1000)
    is_primary: Optional[bool] = Field(None)
    is_visible: Optional[bool] = Field(None)

    @validator('relation')
    def validate_relation(cls, v):
        if v:
            return v.lower().strip()
        return v

    @validator('relationship_notes')
    def validate_notes(cls, v):
        if v:
            return v.strip()
        return v


class UserToMemberResponse(BaseModel):
    id: int
    user_id: int
    member_id: int
    relation: str
    is_shareable: bool
    is_manager: bool
    created_by_user_id: int
    invitation_id: Optional[int]
    relationship_notes: Optional[str]
    is_primary: bool
    is_active: bool
    is_visible: bool
    created_at: datetime
    updated_at: datetime

    # Computed properties
    can_edit: bool
    can_share: bool
    is_derived_relationship: bool

    class Config:
        from_attributes = True


class UserToMemberWithMemberResponse(BaseModel):
    """Response that includes member details"""
    id: int
    user_id: int
    member_id: int
    relation: str
    relationship_display: str
    is_shareable: bool
    is_manager: bool
    relationship_notes: Optional[str]
    is_primary: bool
    is_active: bool
    is_visible: bool
    created_at: datetime
    updated_at: datetime

    # Member details
    member: Dict[str, Any] = Field(..., description="Full member information")

    # Computed properties
    can_edit: bool
    can_share: bool
    is_derived_relationship: bool

    class Config:
        from_attributes = True


class UserToMemberListResponse(BaseModel):
    """Simplified response for listing relationships"""
    id: int
    member_id: int
    member_name: str
    member_age: int
    relationship: str
    relationship_display: str
    is_manager: bool
    is_shareable: bool
    is_primary: bool
    avatar_url: Optional[str]

    class Config:
        from_attributes = True


class FamilyNetworkResponse(BaseModel):
    """Complete family network for a user"""
    user_id: int
    total_members: int
    managed_members: int
    shared_members: int
    relationships: List[UserToMemberWithMemberResponse]
    relationship_types: List[Dict[str, Any]]


class ShareableMembersResponse(BaseModel):
    """Members that can be shared with invited users"""
    user_id: int
    shareable_members: List[UserToMemberListResponse]
    total_shareable: int


class RelationshipPermissionsUpdate(BaseModel):
    """Update just the permissions for a relationship"""
    is_shareable: Optional[bool] = Field(None)
    is_manager: Optional[bool] = Field(None)
    is_visible: Optional[bool] = Field(None)


class RelationshipValidationRequest(BaseModel):
    """Request to validate a new relationship"""
    user_id: int
    member_id: int
    relationship: str


class RelationshipValidationResponse(BaseModel):
    """Response for relationship validation"""
    is_valid: bool
    error_message: Optional[str] = None
    warnings: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None


class RelationshipStatsResponse(BaseModel):
    """Statistics about user's relationships"""
    total_relationships: int
    managed_members: int
    shared_members: int
    derived_relationships: int
    relationship_breakdown: Dict[str, int]  # Count by relationship type
    recent_additions: List[Dict[str, Any]]


class BulkRelationshipCreateRequest(BaseModel):
    """Create multiple relationships at once"""
    relationships: List[UserToMemberCreate] = Field(..., max_items=20)

    @validator('relationships')
    def validate_unique_pairs(cls, v):
        pairs = [(rel.user_id, rel.member_id) for rel in v]
        if len(pairs) != len(set(pairs)):
            raise ValueError('Duplicate user-member pairs in relationship list')
        return v


class BulkRelationshipResponse(BaseModel):
    """Response for bulk relationship operations"""
    total_requested: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]


class RelationshipSearchRequest(BaseModel):
    """Search/filter relationships"""
    user_id: Optional[int] = Field(None)
    member_id: Optional[int] = Field(None)
    relationship_type: Optional[str] = Field(None)
    is_manager: Optional[bool] = Field(None)
    is_shareable: Optional[bool] = Field(None)
    is_active: Optional[bool] = Field(True)
    is_visible: Optional[bool] = Field(True)
    created_after: Optional[datetime] = Field(None)
    created_before: Optional[datetime] = Field(None)


class RelationshipSearchResponse(BaseModel):
    """Response for relationship search"""
    total_found: int
    page: int
    page_size: int
    relationships: List[UserToMemberWithMemberResponse]


class RelationshipTimelineEntry(BaseModel):
    """Entry in relationship timeline/history"""
    id: int
    action: str  # created, updated, shared, hidden, etc.
    timestamp: datetime
    details: Dict[str, Any]
    performed_by_user_id: int


class RelationshipTimelineResponse(BaseModel):
    """Timeline of relationship changes"""
    relationship_id: int
    timeline: List[RelationshipTimelineEntry]