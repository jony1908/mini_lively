"""
RelationshipType CRUD operations.
Handles relationship type management and provides default relationship types.
"""

from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.relationship_type import RelationshipType
from ..schemas.relationship_type import RelationshipTypeCreate, RelationshipTypeUpdate


def create_relationship_type(db: Session, relationship_type: RelationshipTypeCreate) -> RelationshipType:
    """Create a new relationship type"""
    relationship_data = relationship_type.model_dump(exclude_unset=True)
    
    db_relationship_type = RelationshipType(**relationship_data)
    db.add(db_relationship_type)
    db.commit()
    db.refresh(db_relationship_type)
    
    return db_relationship_type


def get_all_relationship_types(db: Session, active_only: bool = True) -> List[RelationshipType]:
    """Get all relationship types"""
    query = db.query(RelationshipType)
    
    if active_only:
        query = query.filter(RelationshipType.is_active == True)
    
    return query.order_by(RelationshipType.sort_order, RelationshipType.display_name).all()


def get_relationship_type_by_id(db: Session, relationship_type_id: int) -> Optional[RelationshipType]:
    """Get a specific relationship type by ID"""
    return db.query(RelationshipType).filter(
        RelationshipType.id == relationship_type_id
    ).first()


def get_relationship_type_by_name(db: Session, name: str) -> Optional[RelationshipType]:
    """Get a specific relationship type by name"""
    return db.query(RelationshipType).filter(
        RelationshipType.name == name.lower().strip(),
        RelationshipType.is_active == True
    ).first()


def update_relationship_type(db: Session, relationship_type_id: int, 
                           relationship_type_update: RelationshipTypeUpdate) -> Optional[RelationshipType]:
    """Update a relationship type's information"""
    db_relationship_type = db.query(RelationshipType).filter(
        RelationshipType.id == relationship_type_id
    ).first()
    
    if not db_relationship_type:
        return None
    
    update_data = relationship_type_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_relationship_type, field, value)
    
    db.commit()
    db.refresh(db_relationship_type)
    
    return db_relationship_type


def delete_relationship_type(db: Session, relationship_type_id: int) -> bool:
    """Soft delete a relationship type (set is_active to False)"""
    db_relationship_type = db.query(RelationshipType).filter(
        RelationshipType.id == relationship_type_id
    ).first()
    
    if not db_relationship_type:
        return False
    
    db_relationship_type.is_active = False
    db.commit()
    return True


def get_relationship_options(db: Session) -> List[RelationshipType]:
    """Get simplified relationship options for dropdowns"""
    return db.query(RelationshipType).filter(
        RelationshipType.is_active == True
    ).order_by(RelationshipType.sort_order, RelationshipType.display_name).all()


def get_reciprocal_relationships(db: Session) -> List[RelationshipType]:
    """Get all reciprocal relationship types (like spouse, sibling)"""
    return db.query(RelationshipType).filter(
        RelationshipType.is_active == True,
        RelationshipType.is_reciprocal == True
    ).order_by(RelationshipType.sort_order).all()


def get_relationships_by_generation(db: Session, generation_offset: int) -> List[RelationshipType]:
    """Get relationships by generation offset"""
    return db.query(RelationshipType).filter(
        RelationshipType.is_active == True,
        RelationshipType.generation_offset == generation_offset
    ).order_by(RelationshipType.sort_order).all()


def find_opposite_relationship(db: Session, relationship_name: str) -> Optional[RelationshipType]:
    """Find the opposite relationship type (e.g., parent -> child)"""
    relationship = get_relationship_type_by_name(db, relationship_name)
    
    if not relationship or not relationship.calculation_rules:
        return None
    
    opposite_name = relationship.calculation_rules.get('opposite')
    if opposite_name:
        return get_relationship_type_by_name(db, opposite_name)
    
    return None


def seed_default_relationship_types(db: Session) -> List[RelationshipType]:
    """Seed the database with default relationship types"""
    default_types = RelationshipType.get_default_relationship_types()
    created_types = []
    
    for type_data in default_types:
        # Check if relationship type already exists
        existing = get_relationship_type_by_name(db, type_data['name'])
        if not existing:
            db_type = RelationshipType(**type_data)
            db.add(db_type)
            created_types.append(db_type)
    
    if created_types:
        db.commit()
        for db_type in created_types:
            db.refresh(db_type)
    
    return created_types


def validate_relationship_name(db: Session, name: str, exclude_id: Optional[int] = None) -> bool:
    """Validate that a relationship name is unique"""
    query = db.query(RelationshipType).filter(
        RelationshipType.name == name.lower().strip()
    )
    
    if exclude_id:
        query = query.filter(RelationshipType.id != exclude_id)
    
    return query.first() is None


def get_relationship_calculation_rules(db: Session, relationship_name: str) -> dict:
    """Get calculation rules for a specific relationship"""
    relationship = get_relationship_type_by_name(db, relationship_name)
    return relationship.calculation_rules if relationship and relationship.calculation_rules else {}


def update_relationship_rules(db: Session, relationship_type_id: int, 
                            calculation_rules: dict) -> Optional[RelationshipType]:
    """Update just the calculation rules for a relationship type"""
    db_relationship_type = db.query(RelationshipType).filter(
        RelationshipType.id == relationship_type_id
    ).first()
    
    if not db_relationship_type:
        return None
    
    db_relationship_type.calculation_rules = calculation_rules
    db.commit()
    db.refresh(db_relationship_type)
    
    return db_relationship_type


def search_relationship_types(db: Session, search_term: str, active_only: bool = True) -> List[RelationshipType]:
    """Search relationship types by name or display name"""
    query = db.query(RelationshipType)
    
    if active_only:
        query = query.filter(RelationshipType.is_active == True)
    
    search_filter = f"%{search_term.lower()}%"
    query = query.filter(
        (RelationshipType.name.ilike(search_filter)) |
        (RelationshipType.display_name.ilike(search_filter))
    )
    
    return query.order_by(RelationshipType.sort_order, RelationshipType.display_name).all()


def get_relationship_usage_stats(db: Session) -> dict:
    """Get usage statistics for relationship types"""
    from ..models.usertomember import UserToMember
    
    # Get count of how many times each relationship type is used
    usage_query = db.query(
        RelationshipType.name,
        RelationshipType.display_name,
        db.func.count(UserToMember.id).label('usage_count')
    ).outerjoin(
        UserToMember, RelationshipType.name == UserToMember.relationship
    ).filter(
        RelationshipType.is_active == True
    ).group_by(
        RelationshipType.name, RelationshipType.display_name
    ).order_by(
        db.func.count(UserToMember.id).desc()
    )
    
    results = usage_query.all()
    
    return {
        "total_types": len(results),
        "total_usage": sum(r.usage_count for r in results),
        "usage_breakdown": [
            {
                "name": r.name,
                "display_name": r.display_name,
                "count": r.usage_count
            }
            for r in results
        ]
    }