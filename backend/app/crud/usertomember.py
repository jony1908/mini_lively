"""
UserToMember CRUD operations.
Handles relationships between users and family members.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List, Dict, Tuple
from datetime import datetime, timedelta
from ..models.usertomember import UserToMember
from ..models.user import User
from ..models.member import Member
from ..models.relationship_type import RelationshipType
from ..schemas.usertomember import UserToMemberCreate, UserToMemberUpdate
import logging

logger = logging.getLogger(__name__)


def create_user_to_member_relationship(db: Session, relationship: UserToMemberCreate, 
                                     created_by_user_id: Optional[int] = None) -> UserToMember:
    """Create a new user-to-member relationship"""
    
    # Validate the relationship doesn't already exist
    existing = get_user_member_relationship(db, relationship.user_id, relationship.member_id)
    if existing:
        raise ValueError("Relationship already exists between this user and member")
    
    # Validate relationship type exists
    rel_type = db.query(RelationshipType).filter(
        RelationshipType.name == relationship.relation,
        RelationshipType.is_active == True
    ).first()
    if not rel_type:
        raise ValueError(f"Invalid relationship type: {relationship.relation}")
    
    # Create the relationship
    db_relationship = UserToMember.create_relationship(
        user_id=relationship.user_id,
        member_id=relationship.member_id,
        relation=relationship.relation,
        created_by_user_id=created_by_user_id or relationship.user_id,
        is_shareable=relationship.is_shareable,
        is_manager=relationship.is_manager,
        relationship_notes=relationship.relationship_notes,
        is_primary=relationship.is_primary
    )
    
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    
    logger.info(f"Created relationship: User {relationship.user_id} -> Member {relationship.member_id} ({relationship.relationship})")
    
    return db_relationship


def get_user_member_relationship(db: Session, user_id: int, member_id: int) -> Optional[UserToMember]:
    """Get a specific relationship between user and member"""
    return db.query(UserToMember).filter(
        UserToMember.user_id == user_id,
        UserToMember.member_id == member_id,
        UserToMember.is_active == True
    ).first()


def get_relationship_by_id(db: Session, relationship_id: int) -> Optional[UserToMember]:
    """Get a specific relationship by ID"""
    return db.query(UserToMember).filter(UserToMember.id == relationship_id).first()


def get_user_members(db: Session, user_id: int, active_only: bool = True, 
                    visible_only: bool = True, relation_type: str = None,
                    include_member_details: bool = False) -> List[UserToMember]:
    """Get all members for a specific user"""
    query = db.query(UserToMember)
    
    if include_member_details:
        query = query.options(joinedload(UserToMember.member))
    
    query = query.filter(UserToMember.user_id == user_id)
    
    if active_only:
        query = query.filter(UserToMember.is_active == True)
    if visible_only:
        query = query.filter(UserToMember.is_visible == True)
    if relation_type:
        query = query.filter(UserToMember.relation == relation_type)
    
    return query.order_by(UserToMember.created_at.desc()).all()


def get_member_users(db: Session, member_id: int, active_only: bool = True) -> List[UserToMember]:
    """Get all users who have a relationship with a specific member"""
    query = db.query(UserToMember).options(joinedload(UserToMember.user))
    query = query.filter(UserToMember.member_id == member_id)
    
    if active_only:
        query = query.filter(UserToMember.is_active == True)
    
    return query.order_by(UserToMember.created_at.desc()).all()


def get_shareable_members(db: Session, user_id: int) -> List[UserToMember]:
    """Get all members that a user can share with invited users"""
    return db.query(UserToMember).options(joinedload(UserToMember.member)).filter(
        UserToMember.user_id == user_id,
        UserToMember.is_active == True,
        UserToMember.is_visible == True,
        UserToMember.is_shareable == True,
        UserToMember.is_manager == True
    ).order_by(UserToMember.created_at.desc()).all()


def get_managed_members(db: Session, user_id: int) -> List[UserToMember]:
    """Get all members that a user can manage (edit/delete)"""
    return db.query(UserToMember).options(joinedload(UserToMember.member)).filter(
        UserToMember.user_id == user_id,
        UserToMember.is_active == True,
        UserToMember.is_manager == True
    ).order_by(UserToMember.created_at.desc()).all()


def update_relationship(db: Session, relationship_id: int, 
                       relationship_update: UserToMemberUpdate) -> Optional[UserToMember]:
    """Update a user-to-member relationship"""
    db_relationship = db.query(UserToMember).filter(
        UserToMember.id == relationship_id
    ).first()
    
    if not db_relationship:
        return None
    
    # If updating relationship type, validate it exists
    update_data = relationship_update.model_dump(exclude_unset=True)
    if 'relationship' in update_data:
        rel_type = db.query(RelationshipType).filter(
            RelationshipType.name == update_data['relationship'],
            RelationshipType.is_active == True
        ).first()
        if not rel_type:
            raise ValueError(f"Invalid relationship type: {update_data['relationship']}")
    
    for field, value in update_data.items():
        setattr(db_relationship, field, value)
    
    db.commit()
    db.refresh(db_relationship)
    
    logger.info(f"Updated relationship {relationship_id}")
    
    return db_relationship


def update_relationship_permissions(db: Session, relationship_id: int, 
                                  is_shareable: Optional[bool] = None,
                                  is_manager: Optional[bool] = None,
                                  is_visible: Optional[bool] = None) -> Optional[UserToMember]:
    """Update just the permissions for a relationship"""
    db_relationship = db.query(UserToMember).filter(
        UserToMember.id == relationship_id
    ).first()
    
    if not db_relationship:
        return None
    
    if is_shareable is not None:
        db_relationship.is_shareable = is_shareable
    if is_manager is not None:
        db_relationship.is_manager = is_manager
    if is_visible is not None:
        db_relationship.is_visible = is_visible
    
    db_relationship.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_relationship)
    
    return db_relationship


def delete_relationship(db: Session, relationship_id: int) -> bool:
    """Soft delete a user-to-member relationship"""
    db_relationship = db.query(UserToMember).filter(
        UserToMember.id == relationship_id
    ).first()
    
    if not db_relationship:
        return False
    
    db_relationship.soft_delete()
    db.commit()
    
    logger.info(f"Soft deleted relationship {relationship_id}")
    
    return True


def hard_delete_relationship(db: Session, relationship_id: int) -> bool:
    """Permanently delete a user-to-member relationship"""
    db_relationship = db.query(UserToMember).filter(
        UserToMember.id == relationship_id
    ).first()
    
    if not db_relationship:
        return False
    
    db.delete(db_relationship)
    db.commit()
    
    logger.info(f"Hard deleted relationship {relationship_id}")
    
    return True


def get_family_network(db: Session, user_id: int) -> Dict:
    """Get complete family network for a user"""
    relationships = get_user_members(db, user_id, include_member_details=True)
    
    # Get relationship type information
    relationship_types = db.query(RelationshipType).filter(
        RelationshipType.is_active == True
    ).all()
    
    # Calculate statistics
    total_members = len(relationships)
    managed_members = sum(1 for rel in relationships if rel.is_manager)
    shared_members = sum(1 for rel in relationships if rel.is_shareable and rel.is_manager)
    
    return {
        "user_id": user_id,
        "total_members": total_members,
        "managed_members": managed_members,
        "shared_members": shared_members,
        "relationships": relationships,
        "relationship_types": [
            {
                "name": rt.name,
                "display_name": rt.display_name,
                "description": rt.description
            }
            for rt in relationship_types
        ]
    }


def validate_new_relationship(db: Session, user_id: int, member_id: int, 
                            relationship_type: str) -> Tuple[bool, str]:
    """Validate if a new relationship can be created"""
    # Check if relationship already exists
    existing = get_user_member_relationship(db, user_id, member_id)
    if existing:
        return False, f"Relationship already exists: {existing.relationship}"
    
    # Check if relationship type is valid
    rel_type = db.query(RelationshipType).filter(
        RelationshipType.name == relationship_type,
        RelationshipType.is_active == True
    ).first()
    if not rel_type:
        return False, f"Invalid relationship type: {relationship_type}"
    
    # Use relationship calculator for advanced validation
    from ..services.relationship_calculator import RelationshipCalculator
    calculator = RelationshipCalculator(db)
    
    return calculator.validate_relationship_compatibility(user_id, member_id, relationship_type)


def get_relationship_stats(db: Session, user_id: int) -> Dict:
    """Get relationship statistics for a user"""
    relationships = get_user_members(db, user_id, active_only=False, visible_only=False)
    
    # Count by relationship type
    relationship_breakdown = {}
    for rel in relationships:
        if rel.is_active:
            rel_type = rel.relationship
            relationship_breakdown[rel_type] = relationship_breakdown.get(rel_type, 0) + 1
    
    # Recent additions (last 30 days)
    recent_cutoff = datetime.utcnow() - timedelta(days=30)
    recent_additions = [
        {
            "id": rel.id,
            "member_id": rel.member_id,
            "relationship": rel.relationship,
            "created_at": rel.created_at
        }
        for rel in relationships
        if rel.created_at > recent_cutoff and rel.is_active
    ]
    
    return {
        "total_relationships": len([r for r in relationships if r.is_active]),
        "managed_members": len([r for r in relationships if r.is_manager and r.is_active]),
        "shared_members": len([r for r in relationships if r.is_shareable and r.is_manager and r.is_active]),
        "derived_relationships": len([r for r in relationships if r.invitation_id is not None and r.is_active]),
        "relationship_breakdown": relationship_breakdown,
        "recent_additions": recent_additions
    }


def search_relationships(db: Session, user_id: Optional[int] = None, 
                        member_id: Optional[int] = None,
                        relationship_type: Optional[str] = None,
                        is_manager: Optional[bool] = None,
                        is_shareable: Optional[bool] = None,
                        is_active: bool = True,
                        created_after: Optional[datetime] = None,
                        created_before: Optional[datetime] = None,
                        limit: int = 100) -> List[UserToMember]:
    """Search relationships with various filters"""
    query = db.query(UserToMember).options(
        joinedload(UserToMember.member),
        joinedload(UserToMember.user)
    )
    
    if user_id:
        query = query.filter(UserToMember.user_id == user_id)
    if member_id:
        query = query.filter(UserToMember.member_id == member_id)
    if relationship_type:
        query = query.filter(UserToMember.relationship == relationship_type)
    if is_manager is not None:
        query = query.filter(UserToMember.is_manager == is_manager)
    if is_shareable is not None:
        query = query.filter(UserToMember.is_shareable == is_shareable)
    if is_active is not None:
        query = query.filter(UserToMember.is_active == is_active)
    if created_after:
        query = query.filter(UserToMember.created_at >= created_after)
    if created_before:
        query = query.filter(UserToMember.created_at <= created_before)
    
    return query.order_by(desc(UserToMember.created_at)).limit(limit).all()


def get_relationship_suggestions(db: Session, user_id: int, member_id: int) -> List[str]:
    """Get relationship suggestions based on existing family network"""
    # Get existing relationships for this user
    existing_relationships = get_user_members(db, user_id)
    
    # Get all available relationship types
    relationship_types = db.query(RelationshipType).filter(
        RelationshipType.is_active == True
    ).order_by(RelationshipType.sort_order).all()
    
    # Filter out already used relationship types for this member
    used_types = {rel.relationship for rel in existing_relationships}
    
    suggestions = []
    for rel_type in relationship_types:
        if rel_type.name not in used_types:
            suggestions.append(rel_type.name)
    
    return suggestions[:10]  # Return top 10 suggestions


def bulk_create_relationships(db: Session, relationships: List[UserToMemberCreate], 
                            created_by_user_id: int) -> Tuple[List[UserToMember], List[str]]:
    """Create multiple relationships in bulk"""
    created_relationships = []
    errors = []
    
    for i, relationship in enumerate(relationships):
        try:
            # Validate each relationship before creating
            is_valid, error_msg = validate_new_relationship(
                db, relationship.user_id, relationship.member_id, relationship.relationship
            )
            
            if not is_valid:
                errors.append(f"Relationship {i+1}: {error_msg}")
                continue
            
            db_relationship = create_user_to_member_relationship(
                db, relationship, created_by_user_id
            )
            created_relationships.append(db_relationship)
            
        except Exception as e:
            errors.append(f"Relationship {i+1}: {str(e)}")
            db.rollback()  # Rollback this transaction but continue with others
    
    return created_relationships, errors


def cleanup_inactive_relationships(db: Session, days_old: int = 365) -> int:
    """Clean up old inactive relationships"""
    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    
    old_relationships = db.query(UserToMember).filter(
        UserToMember.is_active == False,
        UserToMember.updated_at < cutoff_date
    )
    
    count = old_relationships.count()
    old_relationships.delete(synchronize_session=False)
    
    db.commit()
    
    if count > 0:
        logger.info(f"Cleaned up {count} old inactive relationships")
    
    return count


def get_mutual_connections(db: Session, user1_id: int, user2_id: int) -> List[Dict]:
    """Find mutual family member connections between two users"""
    user1_members = db.query(UserToMember.member_id).filter(
        UserToMember.user_id == user1_id,
        UserToMember.is_active == True
    ).subquery()
    
    user2_members = db.query(UserToMember.member_id).filter(
        UserToMember.user_id == user2_id,
        UserToMember.is_active == True
    ).subquery()
    
    # Find common member IDs
    mutual_member_ids = db.query(user1_members.c.member_id).intersect(
        db.query(user2_members.c.member_id)
    ).all()
    
    mutual_connections = []
    for (member_id,) in mutual_member_ids:
        member = db.query(Member).filter(Member.id == member_id).first()
        user1_rel = get_user_member_relationship(db, user1_id, member_id)
        user2_rel = get_user_member_relationship(db, user2_id, member_id)
        
        if member and user1_rel and user2_rel:
            mutual_connections.append({
                "member_id": member_id,
                "member_name": f"{member.first_name} {member.last_name}",
                "user1_relationship": user1_rel.relationship,
                "user2_relationship": user2_rel.relationship
            })
    
    return mutual_connections