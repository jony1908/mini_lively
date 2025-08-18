from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class UserToMember(Base):
    __tablename__ = "usertomember"

    id = Column(Integer, primary_key=True, index=True)
    
    # Core relationship
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    
    # Relationship type - references RelationshipType.name
    relation = Column(String(50), ForeignKey("relationship_types.name"), nullable=False, index=True)
    
    # Permission and sharing settings
    is_shareable = Column(Boolean, default=True, nullable=False)  # Can this member be shared with invited users
    is_manager = Column(Boolean, default=True, nullable=False)   # Can this user edit/delete the member
    
    # Relationship metadata
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Who created this relationship
    invitation_id = Column(Integer, ForeignKey("user_invitations.id"), nullable=True, index=True)  # If created via invitation
    
    # Relationship context and notes
    relationship_notes = Column(Text, nullable=True)  # Additional context about this relationship
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary relationship (e.g., biological vs step)
    
    # Status and visibility
    is_active = Column(Boolean, default=True, nullable=False)
    is_visible = Column(Boolean, default=True, nullable=False)  # Can be hidden without deletion
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint to prevent duplicate relationships
    __table_args__ = (
        UniqueConstraint('user_id', 'member_id', name='unique_user_member_relationship'),
    )
    
    # Relationships
    user = relationship("User", foreign_keys="UserToMember.user_id", back_populates="member_relationships")
    member = relationship("Member", back_populates="user_relationships")
    relationship_type = relationship("RelationshipType")
    created_by = relationship("User", foreign_keys="UserToMember.created_by_user_id")
    invitation = relationship("UserInvitation")

    def __repr__(self):
        permissions = []
        if self.is_manager:
            permissions.append("manager")
        if self.is_shareable:
            permissions.append("shareable")
        if self.is_primary:
            permissions.append("primary")
        if not self.is_active:
            permissions.append("inactive")
        
        permission_str = f" [{', '.join(permissions)}]" if permissions else ""
        invitation_info = f" via_invite#{self.invitation_id}" if self.invitation_id else ""
        
        return f"<UserToMember(#{self.id}: User#{self.user_id} -> Member#{self.member_id} as {self.relation}{permission_str}{invitation_info})>"

    def __str__(self):
        status = " (inactive)" if not self.is_active else ""
        return f"User {self.user_id} is {self.relation} to Member {self.member_id}{status}"

    @classmethod
    def create_relationship(cls, user_id: int, member_id: int, relation: str,
                          created_by_user_id: int = None, invitation_id: int = None,
                          is_shareable: bool = True, is_manager: bool = True,
                          relationship_notes: str = None, is_primary: bool = False) -> 'UserToMember':
        """Create a new user-to-member relationship"""
        if created_by_user_id is None:
            created_by_user_id = user_id
            
        return cls(
            user_id=user_id,
            member_id=member_id,
            relation=relation,
            created_by_user_id=created_by_user_id,
            invitation_id=invitation_id,
            is_shareable=is_shareable,
            is_manager=is_manager,
            relationship_notes=relationship_notes,
            is_primary=is_primary
        )

    @property
    def can_edit(self) -> bool:
        """Check if the user can edit this member"""
        return self.is_manager and self.is_active

    @property
    def can_share(self) -> bool:
        """Check if this member can be shared with invited users"""
        return self.is_shareable and self.is_active and self.is_manager

    @property
    def is_derived_relationship(self) -> bool:
        """Check if this relationship was created through invitation (derived)"""
        return self.invitation_id is not None

    def update_sharing_permissions(self, is_shareable: bool = None, is_manager: bool = None) -> None:
        """Update sharing and management permissions"""
        if is_shareable is not None:
            self.is_shareable = is_shareable
        if is_manager is not None:
            self.is_manager = is_manager
        self.updated_at = datetime.utcnow()

    def set_visibility(self, is_visible: bool) -> None:
        """Set relationship visibility without deletion"""
        self.is_visible = is_visible
        self.updated_at = datetime.utcnow()

    def soft_delete(self) -> None:
        """Soft delete the relationship"""
        self.is_active = False
        self.is_visible = False
        self.updated_at = datetime.utcnow()

    def add_notes(self, notes: str) -> None:
        """Add or update relationship notes"""
        self.relationship_notes = notes
        self.updated_at = datetime.utcnow()

    def set_primary(self, is_primary: bool = True) -> None:
        """Mark this as the primary relationship for this member"""
        self.is_primary = is_primary
        self.updated_at = datetime.utcnow()

    @classmethod
    def get_user_members(cls, db_session, user_id: int, active_only: bool = True, 
                        visible_only: bool = True, relation_type: str = None):
        """Get all members for a specific user with filtering options"""
        query = db_session.query(cls).filter(cls.user_id == user_id)
        
        if active_only:
            query = query.filter(cls.is_active == True)
        if visible_only:
            query = query.filter(cls.is_visible == True)
        if relation_type:
            query = query.filter(cls.relation == relation_type)
            
        return query.all()

    @classmethod
    def get_member_users(cls, db_session, member_id: int, active_only: bool = True):
        """Get all users who have a relationship with a specific member"""
        query = db_session.query(cls).filter(cls.member_id == member_id)
        
        if active_only:
            query = query.filter(cls.is_active == True)
            
        return query.all()

    @classmethod
    def get_shareable_members(cls, db_session, user_id: int):
        """Get all members that a user can share with invited users"""
        return db_session.query(cls).filter(
            cls.user_id == user_id,
            cls.is_active == True,
            cls.is_visible == True,
            cls.is_shareable == True,
            cls.is_manager == True
        ).all()

    @classmethod
    def check_relationship_exists(cls, db_session, user_id: int, member_id: int) -> bool:
        """Check if a relationship already exists between user and member"""
        return db_session.query(cls).filter(
            cls.user_id == user_id,
            cls.member_id == member_id,
            cls.is_active == True
        ).first() is not None