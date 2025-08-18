"""
Member management endpoints.
Handles member profile operations.
"""

import os
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.connection import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse, MemberListResponse, MemberOptionsResponse
from app.utils.image_processing import ImageProcessor
from app.crud.member import (
    create_member,
    get_all_members,
    get_member_by_id,
    update_member,
    delete_member,
    get_member_options
)


router = APIRouter(prefix="/members", tags=["members"])


# Storage configuration
UPLOAD_DIR = "uploads/member_avatars"
BASE_URL = "http://localhost:8000"  # Configure based on environment


async def ensure_upload_dir():
    """Ensure upload directory exists."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def add_member(
    member: MemberCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new member profile.
    
    - Validates member information including interests and skills
    - Returns complete member profile with calculated age
    """
    try:
        new_member = create_member(db, member)
        return new_member
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create member profile: {str(e)}"
        )


@router.get("/", response_model=List[MemberListResponse])
async def get_members(
    db: Session = Depends(get_db),
    include_inactive: bool = False
):
    """
    Get all members.
    
    - Returns list of members with basic information
    - By default, only returns active members
    - Set include_inactive=true to get all members
    """
    members = get_all_members(db, active_only=not include_inactive)
    return members


@router.get("/options", response_model=MemberOptionsResponse)
async def get_member_form_options():
    """
    Get predefined options for member interests and skills.
    
    - Returns lists of common interests and skills
    - Used to populate multi-select dropdowns in frontend
    - No authentication required as options are static
    """
    options = get_member_options()
    return MemberOptionsResponse(**options)


@router.get("/{member_id}", response_model=MemberResponse)
async def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific member by ID.
    
    - Returns complete member profile including interests and skills
    - Returns 404 if member not found
    """
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return member


@router.put("/{member_id}", response_model=MemberResponse)
async def update_member_profile(
    member_id: int,
    member_update: MemberUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a member's profile information.
    
    - Updates only provided fields (partial updates supported)
    - Validates all updated information
    - Returns updated member profile
    """
    updated_member = update_member(db, member_id, member_update)
    if not updated_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return updated_member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member_profile(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a member's profile (soft delete).
    
    - Sets member as inactive rather than permanent deletion
    - Returns 404 if member not found
    """
    success = delete_member(db, member_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )


@router.post("/{member_id}/avatar", response_model=Dict[str, Any])
async def upload_member_avatar(
    member_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process avatar image for a specific member.
    
    - Validates image format and size
    - Resizes to standard avatar dimensions (256x256)
    - Saves optimized image to storage
    - Updates member profile with new avatar URL
    
    Returns:
        Dict containing avatar URL and processing info
    """
    # Verify member exists
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read file data
        file_data = await file.read()
        
        # Validate image format
        if not ImageProcessor.validate_image_format(file_data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported image format. Please use JPEG, PNG, or WEBP"
            )
        
        # Process image
        processed_data, new_filename = ImageProcessor.process_avatar(
            file_data, 
            f"member_{member_id}_{file.filename or 'avatar.jpg'}"
        )
        
        # Ensure upload directory exists
        await ensure_upload_dir()
        
        # Save processed image
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(processed_data)
        
        # Generate public URL
        avatar_url = f"{BASE_URL}/uploads/member_avatars/{new_filename}"
        
        # Update member profile with new avatar URL
        update_data = MemberUpdate(avatar_url=avatar_url)
        updated_member = update_member(db, member_id, update_data)
        
        return {
            "success": True,
            "avatar_url": avatar_url,
            "filename": new_filename,
            "size": len(processed_data),
            "dimensions": f"{ImageProcessor.AVATAR_SIZE[0]}x{ImageProcessor.AVATAR_SIZE[1]}",
            "message": f"Avatar uploaded for {member.first_name} {member.last_name} successfully"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload avatar: {str(e)}"
        )


@router.delete("/{member_id}/avatar")
async def remove_member_avatar(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Remove a member's avatar image.
    
    - Deletes avatar file from storage
    - Updates member profile to remove avatar URL
    
    Returns:
        Success confirmation
    """
    # Verify member exists
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    if not member.avatar_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No avatar found to remove"
        )
    
    try:
        # Extract filename from URL and delete file
        avatar_url = member.avatar_url
        if avatar_url.startswith(BASE_URL):
            filename = os.path.basename(avatar_url)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # Delete file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Update member profile to remove avatar URL
        update_data = MemberUpdate(avatar_url=None)
        update_member(db, member_id, update_data)
        
        return {
            "success": True,
            "message": f"Avatar removed for {member.first_name} {member.last_name} successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove avatar: {str(e)}"
        )


@router.get("/{member_id}/avatar")
async def get_member_avatar_info(
    member_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a member's avatar information.
    
    - Returns avatar URL and metadata if exists
    
    Returns:
        Avatar URL and metadata if exists
    """
    # Verify member exists
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    if not member.avatar_url:
        return {
            "has_avatar": False,
            "avatar_url": None,
            "member_name": f"{member.first_name} {member.last_name}"
        }
    
    return {
        "has_avatar": True,
        "avatar_url": member.avatar_url,
        "member_name": f"{member.first_name} {member.last_name}",
        "upload_limits": {
            "max_size_mb": ImageProcessor.MAX_FILE_SIZE // (1024 * 1024),
            "supported_formats": list(ImageProcessor.SUPPORTED_FORMATS),
            "output_size": f"{ImageProcessor.AVATAR_SIZE[0]}x{ImageProcessor.AVATAR_SIZE[1]}"
        }
    }