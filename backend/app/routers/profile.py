from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..database.connection import get_db
from ..routers.auth import get_current_user
from ..crud import profile as profile_crud
from ..schemas.profile import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from ..models.user import User

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=Optional[UserProfileResponse])
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    profile = profile_crud.get_user_profile(db, current_user.id)
    return profile


@router.post("", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create user profile"""
    # Check if profile already exists
    existing_profile = profile_crud.get_user_profile(db, current_user.id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists. Use PUT to update."
        )
    
    profile = profile_crud.create_user_profile(db, profile_data, current_user.id)
    return profile


@router.put("", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    # Check if profile exists, create if not
    existing_profile = profile_crud.get_user_profile(db, current_user.id)
    if not existing_profile:
        # Convert update to create
        create_data = UserProfileCreate(**profile_data.model_dump(exclude_unset=True))
        profile = profile_crud.create_user_profile(db, create_data, current_user.id)
    else:
        profile = profile_crud.update_user_profile(db, current_user.id, profile_data)
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return profile


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user profile"""
    success = profile_crud.delete_user_profile(db, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )