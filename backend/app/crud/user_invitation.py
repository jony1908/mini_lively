"""
UserInvitation CRUD operations.
Handles invitation management between users for family network sharing.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from ..models.user_invitation import UserInvitation, InvitationStatus
from ..models.user import User
from ..models.usertomember import UserToMember
from ..models.member import Member
from ..schemas.user_invitation import UserInvitationCreate, UserInvitationUpdate
import logging

logger = logging.getLogger(__name__)


def create_invitation(db: Session, invitation: UserInvitationCreate, 
                     inviter_user_id: int) -> UserInvitation:
    """Create a new user invitation"""
    
    # Check if invitee email is already a user
    existing_user = db.query(User).filter(User.email == invitation.invitee_email.lower()).first()
    if existing_user and existing_user.id == inviter_user_id:
        raise ValueError("Cannot invite yourself")
    
    # Check for existing pending invitation
    existing_invitation = db.query(UserInvitation).filter(
        UserInvitation.inviter_user_id == inviter_user_id,
        UserInvitation.invitee_email == invitation.invitee_email.lower(),
        UserInvitation.status == InvitationStatus.PENDING
    ).first()
    
    if existing_invitation and not existing_invitation.is_expired:
        raise ValueError("Pending invitation already exists for this email")
    
    # Create the invitation
    db_invitation = UserInvitation.create_invitation(
        inviter_user_id=inviter_user_id,
        invitee_email=invitation.invitee_email,
        invitation_message=invitation.invitation_message,
        intended_relationship=invitation.intended_relationship,
        share_all_members=invitation.share_all_members,
        specific_member_ids=invitation.specific_member_ids,
        expires_in_days=invitation.expires_in_days
    )
    
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    
    logger.info(f"Created invitation {db_invitation.id} from user {inviter_user_id} to {invitation.invitee_email}")
    
    return db_invitation


def get_invitation_by_id(db: Session, invitation_id: int) -> Optional[UserInvitation]:
    """Get a specific invitation by ID"""
    return db.query(UserInvitation).filter(UserInvitation.id == invitation_id).first()


def get_invitation_by_token(db: Session, token: str) -> Optional[UserInvitation]:
    """Get a specific invitation by token"""
    return db.query(UserInvitation).filter(UserInvitation.invitation_token == token).first()


def get_sent_invitations(db: Session, inviter_user_id: int, 
                        status: Optional[InvitationStatus] = None,
                        include_expired: bool = False) -> List[UserInvitation]:
    """Get all invitations sent by a user"""
    query = db.query(UserInvitation).filter(UserInvitation.inviter_user_id == inviter_user_id)
    
    if status:
        query = query.filter(UserInvitation.status == status)
    
    if not include_expired:
        query = query.filter(
            or_(
                UserInvitation.status != InvitationStatus.PENDING,
                UserInvitation.expires_at > datetime.utcnow()
            )
        )
    
    return query.order_by(UserInvitation.created_at.desc()).all()


def get_received_invitations(db: Session, invitee_email: str, 
                           status: Optional[InvitationStatus] = None,
                           include_expired: bool = False) -> List[UserInvitation]:
    """Get all invitations received by an email address"""
    query = db.query(UserInvitation).filter(UserInvitation.invitee_email == invitee_email.lower())
    
    if status:
        query = query.filter(UserInvitation.status == status)
    
    if not include_expired:
        query = query.filter(
            or_(
                UserInvitation.status != InvitationStatus.PENDING,
                UserInvitation.expires_at > datetime.utcnow()
            )
        )
    
    return query.order_by(UserInvitation.created_at.desc()).all()


def get_pending_invitations_for_user(db: Session, user_email: str) -> List[UserInvitation]:
    """Get all pending invitations for a specific user email"""
    return db.query(UserInvitation).filter(
        UserInvitation.invitee_email == user_email.lower(),
        UserInvitation.status == InvitationStatus.PENDING,
        UserInvitation.expires_at > datetime.utcnow()
    ).order_by(UserInvitation.created_at.desc()).all()


def update_invitation(db: Session, invitation_id: int, 
                     invitation_update: UserInvitationUpdate) -> Optional[UserInvitation]:
    """Update an invitation's information (only if pending)"""
    db_invitation = db.query(UserInvitation).filter(
        UserInvitation.id == invitation_id
    ).first()
    
    if not db_invitation:
        return None
    
    if not db_invitation.is_pending:
        raise ValueError("Cannot update invitation that is not pending")
    
    update_data = invitation_update.model_dump(exclude_unset=True)
    
    # Handle specific_member_ids conversion
    if 'specific_member_ids' in update_data and update_data['specific_member_ids'] is not None:
        import json
        update_data['specific_member_ids'] = json.dumps(update_data['specific_member_ids'])
    
    for field, value in update_data.items():
        setattr(db_invitation, field, value)
    
    db.commit()
    db.refresh(db_invitation)
    
    return db_invitation


def accept_invitation(db: Session, invitation_token: str, invitee_user_id: int) -> Tuple[UserInvitation, List]:
    """Accept an invitation and create relationships"""
    invitation = get_invitation_by_token(db, invitation_token)
    
    if not invitation:
        raise ValueError("Invitation not found")
    
    if not invitation.is_pending:
        raise ValueError("Invitation is not in a state that can be accepted")
    
    # Verify the invitee email matches the user
    invitee_user = db.query(User).filter(User.id == invitee_user_id).first()
    if not invitee_user or invitee_user.email.lower() != invitation.invitee_email.lower():
        raise ValueError("Invitation email does not match user email")
    
    # Accept the invitation
    invitation.accept(invitee_user_id)
    
    # Process relationship creation using the calculator service
    from ..services.relationship_calculator import RelationshipCalculator
    calculator = RelationshipCalculator(db)
    
    created_relationships = calculator.process_invitation_acceptance(invitation, invitee_user_id)
    
    db.commit()
    
    logger.info(f"Accepted invitation {invitation.id}: created {len(created_relationships)} relationships")
    
    return invitation, created_relationships


def decline_invitation(db: Session, invitation_token: str, decline_reason: str = None) -> UserInvitation:
    """Decline an invitation"""
    invitation = get_invitation_by_token(db, invitation_token)
    
    if not invitation:
        raise ValueError("Invitation not found")
    
    if not invitation.is_pending:
        raise ValueError("Invitation is not in a state that can be declined")
    
    invitation.decline()
    
    if decline_reason:
        invitation.relationship_context = f"Declined: {decline_reason}"
    
    db.commit()
    db.refresh(invitation)
    
    logger.info(f"Declined invitation {invitation.id}")
    
    return invitation


def cancel_invitation(db: Session, invitation_id: int, user_id: int) -> bool:
    """Cancel an invitation (by the inviter)"""
    invitation = db.query(UserInvitation).filter(
        UserInvitation.id == invitation_id,
        UserInvitation.inviter_user_id == user_id
    ).first()
    
    if not invitation:
        return False
    
    if invitation.status != InvitationStatus.PENDING:
        raise ValueError("Only pending invitations can be cancelled")
    
    invitation.cancel()
    db.commit()
    
    logger.info(f"Cancelled invitation {invitation_id}")
    
    return True


def expire_old_invitations(db: Session) -> int:
    """Mark expired invitations as expired"""
    expired_invitations = db.query(UserInvitation).filter(
        UserInvitation.status == InvitationStatus.PENDING,
        UserInvitation.expires_at <= datetime.utcnow()
    ).all()
    
    count = 0
    for invitation in expired_invitations:
        invitation.mark_expired()
        count += 1
    
    if count > 0:
        db.commit()
        logger.info(f"Marked {count} invitations as expired")
    
    return count


def get_invitation_preview(db: Session, invitation_token: str) -> dict:
    """Get a preview of what accepting an invitation would create"""
    invitation = get_invitation_by_token(db, invitation_token)
    
    if not invitation or not invitation.is_pending:
        return {}
    
    # Get inviter info
    inviter = db.query(User).filter(User.id == invitation.inviter_user_id).first()
    if not inviter:
        return {}
    
    # Get members that would be shared
    members_to_share = []
    member_relationships = []
    
    if invitation.share_all_members:
        member_relationships = db.query(UserToMember).filter(
            UserToMember.user_id == invitation.inviter_user_id,
            UserToMember.is_active == True,
            UserToMember.is_shareable == True,
            UserToMember.is_manager == True
        ).all()
    else:
        member_ids = invitation.get_member_ids_to_share()
        if member_ids:
            member_relationships = db.query(UserToMember).filter(
                UserToMember.user_id == invitation.inviter_user_id,
                UserToMember.member_id.in_(member_ids),
                UserToMember.is_active == True,
                UserToMember.is_shareable == True
            ).all()
    
    # Get member details and calculate relationships
    from ..services.relationship_calculator import RelationshipCalculator
    calculator = RelationshipCalculator(db)
    
    for member_rel in member_relationships:
        member = db.query(Member).filter(Member.id == member_rel.member_id).first()
        if member:
            derived_relationship = calculator.calculate_derived_relationship(
                member_rel.relationship,
                invitation.intended_relationship or "family"
            )
            
            members_to_share.append({
                "id": member.id,
                "name": f"{member.first_name} {member.last_name}",
                "age": member.age,
                "current_relationship": member_rel.relationship,
                "derived_relationship": derived_relationship,
                "avatar_url": member.avatar_url
            })
    
    return {
        "invitation_id": invitation.id,
        "inviter_name": f"{inviter.first_name or ''} {inviter.last_name or ''}".strip() or inviter.email,
        "intended_relationship": invitation.intended_relationship,
        "relationship_context": invitation.relationship_context,
        "invitation_message": invitation.invitation_message,
        "members_to_share": members_to_share,
        "expires_at": invitation.expires_at
    }


def get_invitation_stats(db: Session, user_id: int) -> dict:
    """Get invitation statistics for a user"""
    sent_stats = db.query(
        UserInvitation.status,
        db.func.count(UserInvitation.id).label('count')
    ).filter(
        UserInvitation.inviter_user_id == user_id
    ).group_by(UserInvitation.status).all()
    
    received_stats = db.query(
        UserInvitation.status,
        db.func.count(UserInvitation.id).label('count')
    ).filter(
        UserInvitation.invitee_user_id == user_id
    ).group_by(UserInvitation.status).all()
    
    sent_dict = {status.value: 0 for status in InvitationStatus}
    received_dict = {status.value: 0 for status in InvitationStatus}
    
    for stat in sent_stats:
        sent_dict[stat.status.value] = stat.count
    
    for stat in received_stats:
        received_dict[stat.status.value] = stat.count
    
    return {
        "sent_total": sum(sent_dict.values()),
        "sent_pending": sent_dict["pending"],
        "sent_accepted": sent_dict["accepted"],
        "sent_declined": sent_dict["declined"],
        "sent_expired": sent_dict["expired"],
        "received_total": sum(received_dict.values()),
        "received_pending": received_dict["pending"]
    }


def cleanup_old_invitations(db: Session, days_old: int = 90) -> int:
    """Clean up old invitations (delete expired/declined invitations older than specified days)"""
    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    
    old_invitations = db.query(UserInvitation).filter(
        UserInvitation.status.in_([InvitationStatus.EXPIRED, InvitationStatus.DECLINED]),
        UserInvitation.updated_at < cutoff_date
    )
    
    count = old_invitations.count()
    old_invitations.delete(synchronize_session=False)
    
    db.commit()
    
    if count > 0:
        logger.info(f"Cleaned up {count} old invitations")
    
    return count


def get_invitations_by_relationship(db: Session, user_id: int, 
                                  intended_relationship: str) -> List[UserInvitation]:
    """Get invitations by intended relationship type"""
    return db.query(UserInvitation).filter(
        UserInvitation.inviter_user_id == user_id,
        UserInvitation.intended_relationship == intended_relationship
    ).order_by(UserInvitation.created_at.desc()).all()


def validate_invitation_email(db: Session, inviter_user_id: int, invitee_email: str) -> Tuple[bool, str]:
    """Validate if an email can be invited"""
    invitee_email = invitee_email.lower().strip()
    
    # Check if trying to invite self
    inviter = db.query(User).filter(User.id == inviter_user_id).first()
    if inviter and inviter.email.lower() == invitee_email:
        return False, "Cannot invite yourself"
    
    # Check for existing pending invitation
    existing = db.query(UserInvitation).filter(
        UserInvitation.inviter_user_id == inviter_user_id,
        UserInvitation.invitee_email == invitee_email,
        UserInvitation.status == InvitationStatus.PENDING,
        UserInvitation.expires_at > datetime.utcnow()
    ).first()
    
    if existing:
        return False, "Pending invitation already exists for this email"
    
    # Check if already connected (if invitee is a user)
    invitee_user = db.query(User).filter(User.email == invitee_email).first()
    if invitee_user:
        # Check if they already have relationships (connected through previous invitation)
        existing_connection = db.query(UserInvitation).filter(
            or_(
                and_(
                    UserInvitation.inviter_user_id == inviter_user_id,
                    UserInvitation.invitee_user_id == invitee_user.id
                ),
                and_(
                    UserInvitation.inviter_user_id == invitee_user.id,
                    UserInvitation.invitee_user_id == inviter_user_id
                )
            ),
            UserInvitation.status == InvitationStatus.ACCEPTED
        ).first()
        
        if existing_connection:
            return False, "Already connected to this user"
    
    return True, ""