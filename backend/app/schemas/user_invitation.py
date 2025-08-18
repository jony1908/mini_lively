from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class InvitationStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class UserInvitationBase(BaseModel):
    invitee_email: EmailStr = Field(..., description="Email address of the person being invited")
    invitation_message: Optional[str] = Field(None, max_length=1000, description="Personal message for the invitation")
    intended_relationship: Optional[str] = Field(None, max_length=50, description="Intended relationship type (spouse, sibling, etc.)")
    relationship_context: Optional[str] = Field(None, max_length=500, description="Additional context about the relationship")
    share_all_members: bool = Field(default=True, description="Whether to share all family members or only specific ones")
    specific_member_ids: Optional[List[int]] = Field(None, description="Specific member IDs to share if not sharing all")

    @validator('invitee_email')
    def validate_email(cls, v):
        return v.lower().strip()

    @validator('invitation_message')
    def validate_message(cls, v):
        if v:
            return v.strip()
        return v

    @validator('specific_member_ids')
    def validate_member_ids(cls, v, values):
        if not values.get('share_all_members', True) and not v:
            raise ValueError('Must specify member IDs when not sharing all members')
        if values.get('share_all_members', True) and v:
            raise ValueError('Cannot specify member IDs when sharing all members')
        return v


class UserInvitationCreate(UserInvitationBase):
    expires_in_days: int = Field(default=7, ge=1, le=30, description="Number of days until invitation expires")


class UserInvitationUpdate(BaseModel):
    invitation_message: Optional[str] = Field(None, max_length=1000)
    intended_relationship: Optional[str] = Field(None, max_length=50)
    relationship_context: Optional[str] = Field(None, max_length=500)
    share_all_members: Optional[bool] = Field(None)
    specific_member_ids: Optional[List[int]] = Field(None)

    @validator('invitation_message')
    def validate_message(cls, v):
        if v:
            return v.strip()
        return v


class UserInvitationResponse(BaseModel):
    id: int
    inviter_user_id: int
    invitee_email: str
    invitee_user_id: Optional[int]
    invitation_token: str
    invitation_message: Optional[str]
    status: InvitationStatusEnum
    intended_relationship: Optional[str]
    relationship_context: Optional[str]
    share_all_members: bool
    specific_member_ids: Optional[List[int]]
    expires_at: datetime
    responded_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Computed properties
    is_expired: bool
    is_pending: bool

    class Config:
        from_attributes = True

    @validator('specific_member_ids', pre=True)
    def parse_member_ids(cls, v):
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return None
        return v


class UserInvitationListResponse(BaseModel):
    """Simplified response for listing invitations"""
    id: int
    invitee_email: str
    status: InvitationStatusEnum
    intended_relationship: Optional[str]
    expires_at: datetime
    created_at: datetime
    is_expired: bool
    is_pending: bool

    class Config:
        from_attributes = True


class ReceivedInvitationResponse(BaseModel):
    """Response for invitations received by a user"""
    id: int
    invitation_token: str
    inviter_name: str
    inviter_email: str
    invitation_message: Optional[str]
    intended_relationship: Optional[str]
    relationship_context: Optional[str]
    expires_at: datetime
    created_at: datetime
    preview_members: List[dict]  # Preview of family members that would be shared

    class Config:
        from_attributes = True


class InvitationAcceptRequest(BaseModel):
    """Request body for accepting an invitation"""
    invitation_token: str = Field(..., description="The invitation token from the email/link")


class InvitationDeclineRequest(BaseModel):
    """Request body for declining an invitation"""
    invitation_token: str = Field(..., description="The invitation token from the email/link")
    decline_reason: Optional[str] = Field(None, max_length=500, description="Optional reason for declining")


class InvitationPreviewResponse(BaseModel):
    """Preview of what accepting an invitation would create"""
    invitation_id: int
    inviter_name: str
    intended_relationship: Optional[str]
    relationship_context: Optional[str]
    members_to_share: List[dict]
    relationships_to_create: List[dict]
    expires_at: datetime


class InvitationStatsResponse(BaseModel):
    """Statistics about user's invitations"""
    sent_total: int
    sent_pending: int
    sent_accepted: int
    sent_declined: int
    sent_expired: int
    received_total: int
    received_pending: int


class BulkInvitationRequest(BaseModel):
    """Request for sending multiple invitations"""
    invitations: List[UserInvitationCreate] = Field(..., max_items=10, description="List of invitations to send (max 10)")

    @validator('invitations')
    def validate_unique_emails(cls, v):
        emails = [inv.invitee_email for inv in v]
        if len(emails) != len(set(emails)):
            raise ValueError('Duplicate email addresses in invitation list')
        return v


class BulkInvitationResponse(BaseModel):
    """Response for bulk invitation sending"""
    total_requested: int
    successful: int
    failed: int
    results: List[dict]  # List of success/failure details for each invitation