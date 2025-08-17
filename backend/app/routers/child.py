"""
Child management endpoints.
Handles child profile operations for authenticated users.
"""

import os
import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.connection import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse, ChildListResponse, ChildOptionsResponse
from app.utils.image_processing import ImageProcessor
from app.crud.child import (
    create_child,
    get_user_children,
    get_child_by_id,
    update_child,
    delete_child,
    get_child_options
)


router = APIRouter(prefix="/children", tags=["children"])


# Storage configuration
UPLOAD_DIR = "uploads/child_avatars"
BASE_URL = "http://localhost:8000"  # Configure based on environment


async def ensure_upload_dir():
    """Ensure upload directory exists."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def add_child(
    child: ChildCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new child profile for the authenticated user.
    
    - Validates child information including interests and skills
    - Automatically associates child with authenticated user
    - Returns complete child profile with calculated age
    """
    try:
        new_child = create_child(db, child, current_user.id)
        return new_child
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create child profile: {str(e)}"
        )


@router.get("/", response_model=List[ChildListResponse])
async def get_children(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    include_inactive: bool = False
):
    """
    Get all children for the authenticated user.
    
    - Returns list of children with basic information
    - By default, only returns active children
    - Set include_inactive=true to get all children
    """
    children = get_user_children(db, current_user.id, active_only=not include_inactive)
    return children


@router.get("/options", response_model=ChildOptionsResponse)
async def get_child_form_options():
    """
    Get predefined options for child interests and skills.
    
    - Returns lists of common interests and skills
    - Used to populate multi-select dropdowns in frontend
    - No authentication required as options are static
    """
    options = get_child_options()
    return ChildOptionsResponse(**options)


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific child by ID.
    
    - Returns complete child profile including interests and skills
    - Ensures child belongs to authenticated user
    - Returns 404 if child not found or doesn't belong to user
    """
    child = get_child_by_id(db, child_id, current_user.id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    return child


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child_profile(
    child_id: int,
    child_update: ChildUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a child's profile information.
    
    - Updates only provided fields (partial updates supported)
    - Validates all updated information
    - Ensures child belongs to authenticated user
    - Returns updated child profile
    """
    updated_child = update_child(db, child_id, current_user.id, child_update)
    if not updated_child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    return updated_child


@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_child_profile(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a child's profile (soft delete).
    
    - Sets child as inactive rather than permanent deletion
    - Ensures child belongs to authenticated user
    - Returns 404 if child not found or doesn't belong to user
    """
    success = delete_child(db, child_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )


@router.post("/{child_id}/avatar", response_model=Dict[str, Any])
async def upload_child_avatar(
    child_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process avatar image for a specific child.
    
    - Validates image format and size
    - Resizes to standard avatar dimensions (256x256)
    - Saves optimized image to storage
    - Updates child profile with new avatar URL
    - Ensures child belongs to authenticated user
    
    Returns:
        Dict containing avatar URL and processing info
    """
    # Verify child exists and belongs to user
    child = get_child_by_id(db, child_id, current_user.id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
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
            f"child_{child_id}_{file.filename or 'avatar.jpg'}"
        )
        
        # Ensure upload directory exists
        await ensure_upload_dir()
        
        # Save processed image
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(processed_data)
        
        # Generate public URL
        avatar_url = f"{BASE_URL}/uploads/child_avatars/{new_filename}"
        
        # Update child profile with new avatar URL
        update_data = ChildUpdate(avatar_url=avatar_url)
        updated_child = update_child(db, child_id, current_user.id, update_data)
        
        return {
            "success": True,
            "avatar_url": avatar_url,
            "filename": new_filename,
            "size": len(processed_data),
            "dimensions": f"{ImageProcessor.AVATAR_SIZE[0]}x{ImageProcessor.AVATAR_SIZE[1]}",
            "message": f"Avatar uploaded for {child.first_name} {child.last_name} successfully"
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


@router.delete("/{child_id}/avatar")
async def remove_child_avatar(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a child's avatar image.
    
    - Deletes avatar file from storage
    - Updates child profile to remove avatar URL
    - Ensures child belongs to authenticated user
    
    Returns:
        Success confirmation
    """
    # Verify child exists and belongs to user
    child = get_child_by_id(db, child_id, current_user.id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    if not child.avatar_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No avatar found to remove"
        )
    
    try:
        # Extract filename from URL and delete file
        avatar_url = child.avatar_url
        if avatar_url.startswith(BASE_URL):
            filename = os.path.basename(avatar_url)
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # Delete file if it exists
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Update child profile to remove avatar URL
        update_data = ChildUpdate(avatar_url=None)
        update_child(db, child_id, current_user.id, update_data)
        
        return {
            "success": True,
            "message": f"Avatar removed for {child.first_name} {child.last_name} successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove avatar: {str(e)}"
        )


@router.get("/{child_id}/avatar")
async def get_child_avatar_info(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a child's avatar information.
    
    - Returns avatar URL and metadata if exists
    - Ensures child belongs to authenticated user
    
    Returns:
        Avatar URL and metadata if exists
    """
    # Verify child exists and belongs to user
    child = get_child_by_id(db, child_id, current_user.id)
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    if not child.avatar_url:
        return {
            "has_avatar": False,
            "avatar_url": None,
            "child_name": f"{child.first_name} {child.last_name}"
        }
    
    return {
        "has_avatar": True,
        "avatar_url": child.avatar_url,
        "child_name": f"{child.first_name} {child.last_name}",
        "upload_limits": {
            "max_size_mb": ImageProcessor.MAX_FILE_SIZE // (1024 * 1024),
            "supported_formats": list(ImageProcessor.SUPPORTED_FORMATS),
            "output_size": f"{ImageProcessor.AVATAR_SIZE[0]}x{ImageProcessor.AVATAR_SIZE[1]}"
        }
    }