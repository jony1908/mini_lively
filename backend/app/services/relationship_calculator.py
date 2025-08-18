"""
Relationship Calculation Service

This service handles the automatic calculation and creation of family relationships
when users accept invitations to join family networks.
"""

from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from ..models.usertomember import UserToMember
from ..models.user_invitation import UserInvitation, InvitationStatus
from ..models.relationship_type import RelationshipType
from ..models.member import Member
import logging

logger = logging.getLogger(__name__)


class RelationshipCalculator:
    """
    Core service for calculating derived relationships when users join family networks
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self._relationship_rules_cache = {}
    
    def get_relationship_rules(self, relationship_name: str) -> Dict:
        """Get calculation rules for a relationship type with caching"""
        if relationship_name not in self._relationship_rules_cache:
            rel_type = self.db.query(RelationshipType).filter(
                RelationshipType.name == relationship_name,
                RelationshipType.is_active == True
            ).first()
            
            if rel_type and rel_type.calculation_rules:
                self._relationship_rules_cache[relationship_name] = rel_type.calculation_rules
            else:
                self._relationship_rules_cache[relationship_name] = {}
        
        return self._relationship_rules_cache[relationship_name]
    
    def calculate_derived_relationship(self, 
                                     inviter_to_member_relationship: str,
                                     inviter_to_invitee_relationship: str) -> Optional[str]:
        """
        Calculate what relationship the invitee should have with a member
        based on the inviter's relationships
        
        Args:
            inviter_to_member_relationship: The inviter's relationship to the member
            inviter_to_invitee_relationship: The intended relationship between inviter and invitee
            
        Returns:
            The calculated relationship name for invitee->member, or None if can't be calculated
        """
        # Get the calculation rules for the inviter's relationship to the member
        member_rules = self.get_relationship_rules(inviter_to_member_relationship)
        
        # Look up the appropriate rule based on the inviter-invitee relationship
        rule_key = f"{inviter_to_invitee_relationship}_relation"
        
        if rule_key in member_rules:
            return member_rules[rule_key]
        
        # Fallback rules for common patterns
        return self._apply_fallback_rules(
            inviter_to_member_relationship, 
            inviter_to_invitee_relationship
        )
    
    def _apply_fallback_rules(self, inviter_member_rel: str, inviter_invitee_rel: str) -> Optional[str]:
        """Apply fallback relationship calculation rules"""
        
        # Common relationship patterns
        fallback_patterns = {
            # If inviter is parent to member
            ("parent", "spouse"): "step_parent",
            ("parent", "sibling"): "aunt_uncle",
            ("parent", "parent"): "grandparent",
            
            # If inviter is child to member  
            ("child", "spouse"): "step_child",
            ("child", "sibling"): "niece_nephew",
            ("child", "child"): "grandchild",
            
            # If inviter is spouse to member
            ("spouse", "child"): "step_child",
            ("spouse", "parent"): "parent_in_law",
            ("spouse", "sibling"): "sibling_in_law",
            
            # If inviter is sibling to member
            ("sibling", "spouse"): "sibling_in_law",
            ("sibling", "child"): "niece_nephew",
            ("sibling", "parent"): "aunt_uncle",
            
            # Grandparent relationships
            ("grandparent", "spouse"): "step_grandparent",
            ("grandchild", "spouse"): "step_grandchild",
        }
        
        return fallback_patterns.get((inviter_member_rel, inviter_invitee_rel))
    
    def process_invitation_acceptance(self, invitation: UserInvitation, 
                                    invitee_user_id: int) -> List[UserToMember]:
        """
        Process an invitation acceptance and create all derived relationships
        
        Args:
            invitation: The accepted UserInvitation
            invitee_user_id: The ID of the user who accepted the invitation
            
        Returns:
            List of created UserToMember relationships
        """
        if invitation.status != InvitationStatus.ACCEPTED:
            raise ValueError("Invitation must be accepted before processing relationships")
        
        created_relationships = []
        
        # Get the members that should be shared based on invitation settings
        members_to_share = self._get_members_to_share(invitation)
        
        logger.info(f"Processing invitation {invitation.id}: sharing {len(members_to_share)} members")
        
        for member_relationship in members_to_share:
            try:
                # Calculate the derived relationship
                derived_relationship = self.calculate_derived_relationship(
                    member_relationship.relation,
                    invitation.intended_relationship or "family"
                )
                
                if derived_relationship:
                    # Check if relationship already exists
                    existing = self.db.query(UserToMember).filter(
                        UserToMember.user_id == invitee_user_id,
                        UserToMember.member_id == member_relationship.member_id,
                        UserToMember.is_active == True
                    ).first()
                    
                    if not existing:
                        # Create the derived relationship
                        new_relationship = UserToMember.create_relationship(
                            user_id=invitee_user_id,
                            member_id=member_relationship.member_id,
                            relation=derived_relationship,
                            created_by_user_id=invitation.inviter_user_id,
                            invitation_id=invitation.id,
                            is_shareable=False,  # Derived relationships can't be shared further
                            is_manager=False,    # Only view access for derived relationships
                            relationship_notes=f"Derived from invitation: {invitation.intended_relationship or 'family'} relationship"
                        )
                        
                        self.db.add(new_relationship)
                        created_relationships.append(new_relationship)
                        
                        logger.info(f"Created derived relationship: User {invitee_user_id} -> Member {member_relationship.member_id} ({derived_relationship})")
                    else:
                        logger.warning(f"Relationship already exists: User {invitee_user_id} -> Member {member_relationship.member_id}")
                else:
                    logger.warning(f"Could not calculate relationship for {member_relationship.relationship} -> {invitation.intended_relationship}")
                    
            except Exception as e:
                logger.error(f"Error creating derived relationship for member {member_relationship.member_id}: {str(e)}")
                continue
        
        # Create direct relationship between inviter and invitee if specified
        if invitation.intended_relationship:
            self._create_direct_user_relationship(
                invitation.inviter_user_id,
                invitee_user_id,
                invitation.intended_relationship,
                invitation
            )
        
        try:
            self.db.commit()
            logger.info(f"Successfully processed invitation {invitation.id}: created {len(created_relationships)} relationships")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error committing relationships for invitation {invitation.id}: {str(e)}")
            raise
        
        return created_relationships
    
    def _get_members_to_share(self, invitation: UserInvitation) -> List[UserToMember]:
        """Get the list of member relationships to share based on invitation settings"""
        base_query = self.db.query(UserToMember).filter(
            UserToMember.user_id == invitation.inviter_user_id,
            UserToMember.is_active == True,
            UserToMember.is_shareable == True,
            UserToMember.is_manager == True  # Only share members the inviter manages
        )
        
        if invitation.share_all_members:
            return base_query.all()
        else:
            # Share only specific members
            member_ids = invitation.get_member_ids_to_share()
            if member_ids:
                return base_query.filter(UserToMember.member_id.in_(member_ids)).all()
            else:
                return []
    
    def _create_direct_user_relationship(self, user1_id: int, user2_id: int, 
                                       relationship: str, invitation: UserInvitation):
        """
        Create direct relationship between two users (for future user-to-user relationships)
        This is a placeholder for future functionality where users have direct relationships
        """
        # TODO: Implement user-to-user relationships when needed
        # For now, we focus on user-to-member relationships
        logger.info(f"Direct user relationship noted: {user1_id} -> {user2_id} ({relationship})")
        pass
    
    def validate_relationship_compatibility(self, user_id: int, member_id: int, 
                                          new_relationship: str) -> Tuple[bool, str]:
        """
        Validate if a new relationship is compatible with existing relationships
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for existing relationships
        existing = self.db.query(UserToMember).filter(
            UserToMember.user_id == user_id,
            UserToMember.member_id == member_id,
            UserToMember.is_active == True
        ).first()
        
        if existing:
            return False, f"Relationship already exists: {existing.relationship}"
        
        # Check for conflicting relationships (e.g., can't be both parent and child)
        conflicting_relationships = self._get_conflicting_relationships(new_relationship)
        
        existing_conflicting = self.db.query(UserToMember).filter(
            UserToMember.user_id == user_id,
            UserToMember.member_id == member_id,
            UserToMember.relationship.in_(conflicting_relationships),
            UserToMember.is_active == True
        ).first()
        
        if existing_conflicting:
            return False, f"Conflicts with existing {existing_conflicting.relationship} relationship"
        
        return True, ""
    
    def _get_conflicting_relationships(self, relationship: str) -> List[str]:
        """Get list of relationships that conflict with the given relationship"""
        conflicts = {
            "parent": ["child", "sibling", "spouse"],
            "child": ["parent", "sibling", "spouse"],
            "spouse": ["parent", "child", "sibling"],
            "sibling": ["parent", "child", "spouse"],
            "grandparent": ["grandchild"],
            "grandchild": ["grandparent"],
        }
        
        return conflicts.get(relationship, [])
    
    def get_relationship_suggestions(self, inviter_user_id: int, 
                                   intended_relationship: str) -> List[Dict]:
        """
        Get suggestions for relationships that will be created when invitation is accepted
        
        Returns:
            List of dictionaries with member info and calculated relationships
        """
        # Get shareable members
        shareable_members = self.db.query(UserToMember).filter(
            UserToMember.user_id == inviter_user_id,
            UserToMember.is_active == True,
            UserToMember.is_shareable == True,
            UserToMember.is_manager == True
        ).all()
        
        suggestions = []
        
        for member_rel in shareable_members:
            derived_rel = self.calculate_derived_relationship(
                member_rel.relationship,
                intended_relationship
            )
            
            if derived_rel:
                member = self.db.query(Member).filter(Member.id == member_rel.member_id).first()
                if member:
                    suggestions.append({
                        "member_id": member.id,
                        "member_name": f"{member.first_name} {member.last_name}",
                        "current_relationship": member_rel.relationship,
                        "derived_relationship": derived_rel,
                        "relationship_display": self._get_relationship_display_name(derived_rel)
                    })
        
        return suggestions
    
    def _get_relationship_display_name(self, relationship_name: str) -> str:
        """Get the display name for a relationship"""
        rel_type = self.db.query(RelationshipType).filter(
            RelationshipType.name == relationship_name
        ).first()
        
        return rel_type.display_name if rel_type else relationship_name.replace("_", " ").title()