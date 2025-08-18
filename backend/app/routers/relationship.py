"""
Family relationship management endpoints.
Handles user-to-member relationships and family network operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.usertomember import (
    UserToMemberCreate, UserToMemberUpdate, UserToMemberResponse,
    UserToMemberWithMemberResponse, UserToMemberListResponse,
    FamilyNetworkResponse, ShareableMembersResponse, RelationshipPermissionsUpdate,
    RelationshipValidationRequest, RelationshipValidationResponse, RelationshipStatsResponse,
    BulkRelationshipCreateRequest, BulkRelationshipResponse, RelationshipSearchRequest,
    RelationshipSearchResponse
)
from app.schemas.relationship_type import RelationshipOptionResponse
from app.crud.usertomember import (
    create_user_to_member_relationship, get_user_members, get_member_users,
    get_shareable_members, get_managed_members, update_relationship,
    update_relationship_permissions, delete_relationship, get_family_network,
    validate_new_relationship, get_relationship_stats, search_relationships,
    get_relationship_suggestions, bulk_create_relationships, get_mutual_connections,
    get_relationship_by_id
)
from app.crud.relationship_type import get_relationship_options
from app.services.relationship_calculator import RelationshipCalculator


router = APIRouter(prefix="/relationships", tags=["relationships"])


@router.post("/", response_model=UserToMemberResponse, status_code=status.HTTP_201_CREATED)
async def create_relationship(
    relationship: UserToMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new user-to-member relationship.
    
    - Validates relationship type and prevents duplicates
    - Only allows creating relationships for yourself or members you manage
    - Returns complete relationship details
    """
    try:
        # Validate relationship
        is_valid, error_msg = validate_new_relationship(
            db, relationship.user_id, relationship.member_id, relationship.relation
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Verify permission to create relationship
        if relationship.user_id != current_user.id:
            # Check if current user manages this member
            managed_members = get_managed_members(db, current_user.id)
            managed_member_ids = [rel.member_id for rel in managed_members]
            
            if relationship.member_id not in managed_member_ids:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only create relationships for members you manage"
                )
        
        new_relationship = create_user_to_member_relationship(
            db, relationship, current_user.id
        )
        
        return new_relationship
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create relationship: {str(e)}"
        )


@router.get("/my-family", response_model=FamilyNetworkResponse)
async def get_my_family_network(
    include_inactive: bool = Query(False, description="Include inactive relationships"),
    relation_type: Optional[str] = Query(None, description="Filter by relationship type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the complete family network for the current user.
    
    - Returns all family members with relationship details
    - Includes relationship type information for reference
    - Supports filtering by relationship type and status
    """
    try:
        family_network = get_family_network(db, current_user.id)
        
        # Apply filters if specified
        if not include_inactive or relation_type:
            filtered_relationships = []
            for rel in family_network["relationships"]:
                if not include_inactive and not rel.is_active:
                    continue
                if relation_type and rel.relation != relation_type:
                    continue
                filtered_relationships.append(rel)
            
            family_network["relationships"] = filtered_relationships
            family_network["total_members"] = len(filtered_relationships)
        
        return FamilyNetworkResponse(**family_network)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve family network: {str(e)}"
        )


@router.get("/member/{member_id}", response_model=List[UserToMemberResponse])
async def get_member_relationships(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all users who have a relationship with a specific member.
    
    - Shows different perspectives on the same family member
    - Useful for understanding complex family dynamics
    - Only shows relationships for members the user has access to
    """
    try:
        # Verify user has access to this member
        user_members = get_user_members(db, current_user.id)
        accessible_member_ids = [rel.member_id for rel in user_members]
        
        if member_id not in accessible_member_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this member"
            )
        
        relationships = get_member_users(db, member_id)
        return relationships
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve member relationships: {str(e)}"
        )


@router.get("/shareable", response_model=ShareableMembersResponse)
async def get_shareable_family_members(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all family members that can be shared with invited users.
    
    - Only includes members the user manages and has marked as shareable
    - Used when creating invitations to show sharing options
    """
    try:
        shareable_rels = get_shareable_members(db, current_user.id)
        
        # Convert to list response format
        shareable_list = []
        for rel in shareable_rels:
            member = rel.member
            shareable_list.append(UserToMemberListResponse(
                id=rel.id,
                member_id=member.id,
                member_name=f"{member.first_name} {member.last_name}",
                member_age=member.age,
                relation=rel.relation,
                relationship_display=rel.relation.replace('_', ' ').title(),
                is_manager=rel.is_manager,
                is_shareable=rel.is_shareable,
                is_primary=rel.is_primary,
                avatar_url=member.avatar_url
            ))
        
        return ShareableMembersResponse(
            user_id=current_user.id,
            shareable_members=shareable_list,
            total_shareable=len(shareable_list)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve shareable members: {str(e)}"
        )


@router.put("/{relationship_id}", response_model=UserToMemberResponse)
async def update_relationship_details(
    relationship_id: int,
    relationship_update: UserToMemberUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update relationship details.
    
    - Allows updating relationship type, permissions, and notes
    - Only managers can update relationship details
    - Validates new relationship types
    """
    try:
        # Verify permission
        relationship = get_relationship_by_id(db, relationship_id)
        if not relationship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found"
            )
        
        # Check if user can modify this relationship
        if (relationship.user_id != current_user.id and 
            relationship.created_by_user_id != current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this relationship"
            )
        
        updated_relationship = update_relationship(db, relationship_id, relationship_update)
        if not updated_relationship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found"
            )
        
        return updated_relationship
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update relationship: {str(e)}"
        )


@router.patch("/{relationship_id}/permissions", response_model=UserToMemberResponse)
async def update_relationship_permissions(
    relationship_id: int,
    permissions: RelationshipPermissionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update only the permissions for a relationship.
    
    - Quick way to change sharing and management permissions
    - Useful for privacy control without full relationship update
    """
    try:
        # Verify permission
        relationship = get_relationship_by_id(db, relationship_id)
        if not relationship or relationship.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found"
            )
        
        updated_relationship = update_relationship_permissions(
            db, relationship_id, 
            permissions.is_shareable, 
            permissions.is_manager,
            permissions.is_visible
        )
        
        return updated_relationship
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update permissions: {str(e)}"
        )


@router.delete("/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_relationship(
    relationship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a family relationship (soft delete).
    
    - Soft deletes the relationship (sets inactive)
    - Only managers can delete relationships
    - Cannot delete relationships created via invitation
    """
    try:
        # Verify permission
        relationship = get_relationship_by_id(db, relationship_id)
        if not relationship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found"
            )
        
        if relationship.user_id != current_user.id or not relationship.is_manager:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this relationship"
            )
        
        if relationship.invitation_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete relationships created via invitation"
            )
        
        success = delete_relationship(db, relationship_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relationship not found"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete relationship: {str(e)}"
        )


@router.post("/validate", response_model=RelationshipValidationResponse)
async def validate_relationship(
    validation_request: RelationshipValidationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Validate if a new relationship can be created.
    
    - Checks for conflicts and duplicates
    - Provides suggestions for valid relationship types
    - Useful for form validation before submission
    """
    try:
        is_valid, error_msg = validate_new_relationship(
            db, validation_request.user_id, 
            validation_request.member_id, validation_request.relation
        )
        
        suggestions = []
        if not is_valid:
            # Get relationship suggestions
            suggestions = get_relationship_suggestions(
                db, validation_request.user_id, validation_request.member_id
            )
        
        return RelationshipValidationResponse(
            is_valid=is_valid,
            error_message=error_msg if not is_valid else None,
            suggestions=suggestions if not is_valid else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate relationship: {str(e)}"
        )


@router.get("/stats", response_model=RelationshipStatsResponse)
async def get_relationship_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get relationship statistics for the current user.
    
    - Shows counts by relationship type
    - Includes recent additions and management info
    - Useful for dashboard displays
    """
    try:
        stats = get_relationship_stats(db, current_user.id)
        return RelationshipStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve relationship statistics: {str(e)}"
        )


@router.post("/search", response_model=RelationshipSearchResponse)
async def search_family_relationships(
    search_request: RelationshipSearchRequest,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search and filter family relationships.
    
    - Advanced filtering by multiple criteria
    - Supports pagination for large families
    - Useful for finding specific relationships
    """
    try:
        # Override user_id to current user if not specified
        if not search_request.user_id:
            search_request.user_id = current_user.id
        
        # Verify permission to search other users' relationships
        if search_request.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only search your own relationships"
            )
        
        relationships = search_relationships(
            db,
            user_id=search_request.user_id,
            member_id=search_request.member_id,
            relationship_type=search_request.relationship_type,
            is_manager=search_request.is_manager,
            is_shareable=search_request.is_shareable,
            is_active=search_request.is_active,
            created_after=search_request.created_after,
            created_before=search_request.created_before,
            limit=page_size
        )
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_relationships = relationships[start_idx:end_idx]
        
        return RelationshipSearchResponse(
            total_found=len(relationships),
            page=page,
            page_size=page_size,
            relationships=paginated_relationships
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search relationships: {str(e)}"
        )


@router.post("/bulk", response_model=BulkRelationshipResponse)
async def create_bulk_relationships(
    bulk_request: BulkRelationshipCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create multiple relationships at once.
    
    - Validates all relationships before creating any
    - Returns success/failure status for each relationship
    - Maximum 20 relationships per request
    """
    try:
        created_relationships, errors = bulk_create_relationships(
            db, bulk_request.relationships, current_user.id
        )
        
        results = []
        for i, relationship in enumerate(bulk_request.relationships):
            if i < len(created_relationships):
                results.append({
                    "user_id": relationship.user_id,
                    "member_id": relationship.member_id,
                    "relation": relationship.relation,
                    "success": True,
                    "relationship_id": created_relationships[i].id
                })
            else:
                error_msg = errors[i - len(created_relationships)] if errors else "Unknown error"
                results.append({
                    "user_id": relationship.user_id,
                    "member_id": relationship.member_id,
                    "relation": relationship.relation,
                    "success": False,
                    "error": error_msg
                })
        
        return BulkRelationshipResponse(
            total_requested=len(bulk_request.relationships),
            successful=len(created_relationships),
            failed=len(errors),
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create bulk relationships: {str(e)}"
        )


@router.get("/mutual-connections/{other_user_id}", response_model=List[dict])
async def get_mutual_family_connections(
    other_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Find mutual family member connections with another user.
    
    - Shows shared family members and how each user relates to them
    - Useful for understanding family network overlaps
    - Helps identify potential relationship conflicts
    """
    try:
        mutual_connections = get_mutual_connections(db, current_user.id, other_user_id)
        return mutual_connections
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to find mutual connections: {str(e)}"
        )


@router.get("/types", response_model=List[RelationshipOptionResponse])
async def get_available_relationship_types(
    db: Session = Depends(get_db)
):
    """
    Get all available relationship types for selection.
    
    - Returns relationship types with display names and descriptions
    - Used to populate dropdown menus and forms
    - No authentication required as types are public reference data
    """
    try:
        relationship_types = get_relationship_options(db)
        
        return [
            RelationshipOptionResponse(
                name=rt.name,
                display_name=rt.display_name,
                description=rt.description,
                is_reciprocal=rt.is_reciprocal
            )
            for rt in relationship_types
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve relationship types: {str(e)}"
        )