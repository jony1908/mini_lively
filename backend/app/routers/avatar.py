"""
Avatar upload and management endpoints.
Handles user profile picture uploads with proper scaling and storage.
"""

import os
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database.connection import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.utils.image_processing import ImageProcessor
from app.crud.profile import get_user_profile, update_user_profile, create_user_profile
from app.schemas.profile import UserProfileCreate, UserProfileUpdate


router = APIRouter(prefix="/avatar", tags=["avatar"])


# Storage configuration
UPLOAD_DIR = "uploads/avatars"
BASE_URL = "http://localhost:8000"  # Configure based on environment


async def ensure_upload_dir():
    """Ensure upload directory exists."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=Dict[str, Any])
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process user avatar image.
    
    - Validates image format and size
    - Resizes to standard avatar dimensions (256x256)
    - Saves optimized image to storage
    - Updates user profile with new avatar URL
    
    Returns:
        Dict containing avatar URL and processing info
    """
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
            file.filename or "avatar.jpg"
        )
        
        # Ensure upload directory exists
        await ensure_upload_dir()
        
        # Save processed image
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(processed_data)
        
        # Generate public URL
        avatar_url = f"{BASE_URL}/uploads/avatars/{new_filename}"
        
        # Update user profile with new avatar URL
        profile = get_user_profile(db, current_user.id)
        if profile:
            # Update existing profile
            update_data = UserProfileUpdate(profile_picture_url=avatar_url)
            updated_profile = update_user_profile(db, current_user.id, update_data)
        else:
            # Create new profile if it doesn't exist
            profile_data = UserProfileCreate(profile_picture_url=avatar_url)
            updated_profile = create_user_profile(db, profile_data, current_user.id)
        
        return {
            "success": True,
            "avatar_url": avatar_url,
            "filename": new_filename,
            "size": len(processed_data),
            "dimensions": f"{ImageProcessor.AVATAR_SIZE[0]}x{ImageProcessor.AVATAR_SIZE[1]}",
            "message": "Avatar uploaded and processed successfully"
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


@router.delete("/remove")
async def remove_avatar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove user's current avatar.
    
    - Deletes avatar file from storage
    - Updates profile to remove avatar URL
    
    Returns:
        Success confirmation
    """
    try:
        # Get current profile
        profile = get_user_profile(db, current_user.id)
        if not profile or not profile.profile_picture_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No avatar found to remove"
            )
        
        # Extract filename from URL
        avatar_url = profile.profile_picture_url
        if avatar_url.startswith(BASE_URL):
            filename = os.path.basename(avatar_url)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # Delete file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Update profile to remove avatar URL
        update_data = UserProfileUpdate(profile_picture_url=None)
        update_user_profile(db, current_user.id, update_data)
        
        return {
            "success": True,
            "message": "Avatar removed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove avatar: {str(e)}"
        )


@router.get("/info")
async def get_avatar_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's avatar information.
    
    Returns:
        Avatar URL and metadata if exists
    """
    profile = get_user_profile(db, current_user.id)
    
    if not profile or not profile.profile_picture_url:
        return {
            "has_avatar": False,
            "avatar_url": None
        }
    
    return {
        "has_avatar": True,
        "avatar_url": profile.profile_picture_url,
        "upload_limits": {
            "max_size_mb": ImageProcessor.MAX_FILE_SIZE // (1024 * 1024),
            "supported_formats": list(ImageProcessor.SUPPORTED_FORMATS),
            "output_size": f"{ImageProcessor.AVATAR_SIZE[0]}x{ImageProcessor.AVATAR_SIZE[1]}"
        }
    }