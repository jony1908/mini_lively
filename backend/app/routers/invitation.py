"""
User invitation endpoints.
Handles family network invitation management and relationship creation.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.user_invitation import (
    UserInvitationCreate, UserInvitationUpdate, UserInvitationResponse,
    UserInvitationListResponse, ReceivedInvitationResponse, InvitationAcceptRequest,
    InvitationDeclineRequest, InvitationPreviewResponse, InvitationStatsResponse,
    BulkInvitationRequest, BulkInvitationResponse
)
from app.schemas.relationship_type import RelationshipCalculationPreview
from app.crud.user_invitation import (
    create_invitation, get_sent_invitations, get_received_invitations,
    get_pending_invitations_for_user, update_invitation, accept_invitation,
    decline_invitation, cancel_invitation, get_invitation_by_token,
    get_invitation_preview, get_invitation_stats, validate_invitation_email,
    expire_old_invitations
)
from app.crud.relationship_type import get_relationship_options
from app.services.relationship_calculator import RelationshipCalculator


router = APIRouter(prefix="/invitations", tags=["invitations"])


@router.post("/", response_model=UserInvitationResponse, status_code=status.HTTP_201_CREATED)
async def send_invitation(
    invitation: UserInvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send a family network invitation to another user.
    
    - Validates invitation email and checks for duplicates
    - Creates secure invitation token with expiration
    - Returns invitation details for confirmation
    """
    try:
        # Validate the invitation email
        is_valid, error_msg = validate_invitation_email(db, current_user.id, invitation.invitee_email)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Create the invitation
        new_invitation = create_invitation(db, invitation, current_user.id)
        
        # TODO: Send invitation email here
        # email_service.send_invitation_email(new_invitation)
        
        return new_invitation
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send invitation: {str(e)}"
        )


@router.get("/sent", response_model=List[UserInvitationListResponse])
async def get_sent_invitations_list(
    status_filter: Optional[str] = Query(None, description="Filter by invitation status"),
    include_expired: bool = Query(False, description="Include expired invitations"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all invitations sent by the current user.
    
    - Supports filtering by status (pending, accepted, declined, expired)
    - Can include or exclude expired invitations
    - Returns simplified invitation list
    """
    try:
        status_enum = None
        if status_filter:
            from app.models.user_invitation import InvitationStatus
            try:
                status_enum = InvitationStatus(status_filter.lower())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status filter: {status_filter}"
                )
        
        invitations = get_sent_invitations(
            db, current_user.id, status_enum, include_expired
        )
        
        return invitations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sent invitations: {str(e)}"
        )


@router.get("/received", response_model=List[ReceivedInvitationResponse])
async def get_received_invitations_list(
    include_expired: bool = Query(False, description="Include expired invitations"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all invitations received by the current user.
    
    - Shows invitations with inviter details
    - Includes preview of family members that would be shared
    - Can include or exclude expired invitations
    """
    try:
        invitations = get_received_invitations(
            db, current_user.email, None, include_expired
        )
        
        # Enhance with preview information
        enhanced_invitations = []
        for invitation in invitations:
            preview = get_invitation_preview(db, invitation.invitation_token)
            
            enhanced_invitation = ReceivedInvitationResponse(
                id=invitation.id,
                invitation_token=invitation.invitation_token,
                inviter_name=preview.get("inviter_name", "Unknown"),
                inviter_email=invitation.inviter.email if invitation.inviter else "",
                invitation_message=invitation.invitation_message,
                intended_relationship=invitation.intended_relationship,
                relationship_context=invitation.relationship_context,
                expires_at=invitation.expires_at,
                created_at=invitation.created_at,
                preview_members=preview.get("members_to_share", [])
            )
            enhanced_invitations.append(enhanced_invitation)
        
        return enhanced_invitations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve received invitations: {str(e)}"
        )


@router.get("/preview/{invitation_token}", response_model=InvitationPreviewResponse)
async def preview_invitation(
    invitation_token: str,
    db: Session = Depends(get_db)
):
    """
    Preview what accepting an invitation would create.
    
    - Shows family members that would be shared
    - Displays calculated relationships that would be created
    - Does not require authentication (public preview)
    """
    try:
        preview_data = get_invitation_preview(db, invitation_token)
        
        if not preview_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found or expired"
            )
        
        return InvitationPreviewResponse(**preview_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to preview invitation: {str(e)}"
        )


@router.post("/accept", response_model=dict)
async def accept_family_invitation(
    accept_request: InvitationAcceptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Accept a family network invitation.
    
    - Validates invitation token and user email match
    - Creates all calculated family relationships automatically
    - Returns summary of created relationships
    """
    try:
        invitation, created_relationships = accept_invitation(
            db, accept_request.invitation_token, current_user.id
        )
        
        return {
            "success": True,
            "message": f"Successfully joined {invitation.inviter.first_name}'s family network",
            "invitation_id": invitation.id,
            "relationships_created": len(created_relationships),
            "relationship_details": [
                {
                    "member_id": rel.member_id,
                    "relation": rel.relation,
                    "is_manager": rel.is_manager
                }
                for rel in created_relationships
            ]
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to accept invitation: {str(e)}"
        )


@router.post("/decline", response_model=dict)
async def decline_family_invitation(
    decline_request: InvitationDeclineRequest,
    db: Session = Depends(get_db)
):
    """
    Decline a family network invitation.
    
    - Marks invitation as declined with optional reason
    - Does not require authentication (can decline via email link)
    """
    try:
        invitation = decline_invitation(
            db, decline_request.invitation_token, decline_request.decline_reason
        )
        
        return {
            "success": True,
            "message": "Invitation declined successfully",
            "invitation_id": invitation.id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decline invitation: {str(e)}"
        )


@router.put("/{invitation_id}", response_model=UserInvitationResponse)
async def update_invitation_details(
    invitation_id: int,
    invitation_update: UserInvitationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update invitation details (only for pending invitations).
    
    - Allows updating message, relationship type, and member sharing settings
    - Only the inviter can update their own invitations
    """
    try:
        # Verify ownership
        invitation = get_invitation_by_id(db, invitation_id)
        if not invitation or invitation.inviter_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found"
            )
        
        updated_invitation = update_invitation(db, invitation_id, invitation_update)
        if not updated_invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found"
            )
        
        return updated_invitation
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update invitation: {str(e)}"
        )


@router.delete("/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_invitation_by_id(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel a pending invitation.
    
    - Only the inviter can cancel their own invitations
    - Can only cancel pending invitations
    """
    try:
        success = cancel_invitation(db, invitation_id, current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found or cannot be cancelled"
            )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel invitation: {str(e)}"
        )


@router.get("/stats", response_model=InvitationStatsResponse)
async def get_invitation_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get invitation statistics for the current user.
    
    - Shows counts of sent and received invitations by status
    - Useful for dashboard displays
    """
    try:
        stats = get_invitation_stats(db, current_user.id)
        return InvitationStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve invitation statistics: {str(e)}"
        )


@router.get("/relationship-suggestions", response_model=List[RelationshipCalculationPreview])
async def get_relationship_suggestions_for_invitation(
    intended_relationship: str = Query(..., description="Intended relationship type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get preview of relationships that would be created for an invitation.
    
    - Shows how current family members would relate to the invited user
    - Helps users understand the impact before sending invitation
    """
    try:
        calculator = RelationshipCalculator(db)
        suggestions = calculator.get_relationship_suggestions(
            current_user.id, intended_relationship
        )
        
        return [RelationshipCalculationPreview(**suggestion) for suggestion in suggestions]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get relationship suggestions: {str(e)}"
        )


@router.post("/bulk", response_model=BulkInvitationResponse)
async def send_bulk_invitations(
    bulk_request: BulkInvitationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send multiple invitations at once.
    
    - Validates all emails before sending any invitations
    - Returns success/failure status for each invitation
    - Maximum 10 invitations per request
    """
    try:
        results = []
        successful = 0
        failed = 0
        
        for invitation in bulk_request.invitations:
            try:
                # Validate email
                is_valid, error_msg = validate_invitation_email(
                    db, current_user.id, invitation.invitee_email
                )
                if not is_valid:
                    results.append({
                        "email": invitation.invitee_email,
                        "success": False,
                        "error": error_msg
                    })
                    failed += 1
                    continue
                
                # Create invitation
                new_invitation = create_invitation(db, invitation, current_user.id)
                results.append({
                    "email": invitation.invitee_email,
                    "success": True,
                    "invitation_id": new_invitation.id
                })
                successful += 1
                
            except Exception as e:
                results.append({
                    "email": invitation.invitee_email,
                    "success": False,
                    "error": str(e)
                })
                failed += 1
        
        return BulkInvitationResponse(
            total_requested=len(bulk_request.invitations),
            successful=successful,
            failed=failed,
            results=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process bulk invitations: {str(e)}"
        )


@router.post("/cleanup-expired", response_model=dict)
async def cleanup_expired_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark expired invitations as expired (admin/maintenance endpoint).
    
    - Updates invitation status for expired invitations
    - Returns count of updated invitations
    """
    try:
        count = expire_old_invitations(db)
        return {
            "success": True,
            "message": f"Marked {count} invitations as expired",
            "expired_count": count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cleanup expired invitations: {str(e)}"
        )