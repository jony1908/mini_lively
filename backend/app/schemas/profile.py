from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class UserProfileBase(BaseModel):
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    preferred_activity_types: Optional[List[str]] = None
    preferred_schedule: Optional[Dict[str, Any]] = None
    notification_preferences: Optional[Dict[str, Any]] = None


class UserProfileUpdate(BaseModel):
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    preferred_activity_types: Optional[List[str]] = None
    preferred_schedule: Optional[Dict[str, Any]] = None
    notification_preferences: Optional[Dict[str, Any]] = None


class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    preferred_activity_types: Optional[List[str]] = None
    preferred_schedule: Optional[Dict[str, Any]] = None
    notification_preferences: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}