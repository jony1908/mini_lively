from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum
import secrets
import string
from .base import Base


class InvitationStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class UserInvitation(Base):
    __tablename__ = "user_invitations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Inviter information
    inviter_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Invitee information
    invitee_email = Column(String(255), nullable=False, index=True)
    invitee_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Set when accepted
    
    # Invitation details
    invitation_token = Column(String(64), unique=True, nullable=False, index=True)
    invitation_message = Column(Text, nullable=True)
    status = Column(Enum(InvitationStatus), default=InvitationStatus.PENDING, nullable=False, index=True)
    
    # Relationship context for invitation
    intended_relationship = Column(String(50), nullable=True)  # e.g., "spouse", "sibling"
    relationship_context = Column(Text, nullable=True)  # Additional context about the relationship
    
    # Member sharing configuration
    share_all_members = Column(Boolean, default=True, nullable=False)
    specific_member_ids = Column(Text, nullable=True)  # JSON array of member IDs to share if not all
    
    # Timing
    expires_at = Column(DateTime, nullable=False)
    responded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    inviter = relationship("User", foreign_keys=[inviter_user_id], back_populates="sent_invitations")
    invitee = relationship("User", foreign_keys=[invitee_user_id], back_populates="received_invitations")

    def __repr__(self):
        return f"<UserInvitation(id={self.id}, inviter_id={self.inviter_user_id}, invitee_email='{self.invitee_email}', status='{self.status.value}')>"

    def __str__(self):
        return f"Invitation from {self.inviter_user_id} to {self.invitee_email} - {self.status.value}"

    @classmethod
    def generate_invitation_token(cls) -> str:
        """Generate a secure random invitation token"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(64))

    @classmethod
    def create_invitation(cls, inviter_user_id: int, invitee_email: str, 
                         invitation_message: str = None,
                         intended_relationship: str = None,
                         share_all_members: bool = True,
                         specific_member_ids: list = None,
                         expires_in_days: int = 7) -> 'UserInvitation':
        """Create a new invitation with proper defaults"""
        token = cls.generate_invitation_token()
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        # Convert member IDs list to JSON string if provided
        member_ids_json = None
        if not share_all_members and specific_member_ids:
            import json
            member_ids_json = json.dumps(specific_member_ids)
        
        return cls(
            inviter_user_id=inviter_user_id,
            invitee_email=invitee_email.lower().strip(),
            invitation_token=token,
            invitation_message=invitation_message,
            intended_relationship=intended_relationship,
            share_all_members=share_all_members,
            specific_member_ids=member_ids_json,
            expires_at=expires_at
        )

    @property
    def is_expired(self) -> bool:
        """Check if the invitation has expired"""
        return datetime.utcnow() > self.expires_at

    @property
    def is_pending(self) -> bool:
        """Check if the invitation is still pending"""
        return self.status == InvitationStatus.PENDING and not self.is_expired

    def accept(self, invitee_user_id: int) -> None:
        """Accept the invitation"""
        if not self.is_pending:
            raise ValueError("Invitation is not in a state that can be accepted")
        
        self.status = InvitationStatus.ACCEPTED
        self.invitee_user_id = invitee_user_id
        self.responded_at = datetime.utcnow()

    def decline(self) -> None:
        """Decline the invitation"""
        if not self.is_pending:
            raise ValueError("Invitation is not in a state that can be declined")
        
        self.status = InvitationStatus.DECLINED
        self.responded_at = datetime.utcnow()

    def cancel(self) -> None:
        """Cancel the invitation (by inviter)"""
        if self.status not in [InvitationStatus.PENDING]:
            raise ValueError("Only pending invitations can be cancelled")
        
        self.status = InvitationStatus.CANCELLED

    def mark_expired(self) -> None:
        """Mark invitation as expired"""
        if self.status == InvitationStatus.PENDING:
            self.status = InvitationStatus.EXPIRED

    def get_member_ids_to_share(self) -> list:
        """Get the list of member IDs to share with invitee"""
        if self.share_all_members:
            return []  # Empty list means all members
        
        if self.specific_member_ids:
            import json
            try:
                return json.loads(self.specific_member_ids)
            except json.JSONDecodeError:
                return []
        
        return []