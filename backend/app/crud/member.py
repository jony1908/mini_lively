"""
Member CRUD operations.
Handles member profile management.
"""

import json
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.member import Member
from ..schemas.member import MemberCreate, MemberUpdate


def create_member(db: Session, member: MemberCreate) -> Member:
    """Create a new member profile"""
    member_data = member.model_dump(exclude_unset=True)
    
    # Convert lists to JSON strings for database storage
    if 'interests' in member_data and member_data['interests']:
        member_data['interests'] = json.dumps(member_data['interests'])
    
    if 'skills' in member_data and member_data['skills']:
        member_data['skills'] = json.dumps(member_data['skills'])
    
    db_member = Member(**member_data)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    
    return get_member_by_id(db, db_member.id)


def get_all_members(db: Session, active_only: bool = True) -> List[Member]:
    """Get all members"""
    query = db.query(Member)
    
    if active_only:
        query = query.filter(Member.is_active == True)
    
    members = query.order_by(Member.created_at.desc()).all()
    
    # Convert JSON strings back to Python objects for API responses
    for member in members:
        if member.interests:
            try:
                member.interests = json.loads(member.interests)
            except json.JSONDecodeError:
                member.interests = None
        
        if member.skills:
            try:
                member.skills = json.loads(member.skills)
            except json.JSONDecodeError:
                member.skills = None
    
    return members


def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    """Get a specific member by ID"""
    member = db.query(Member).filter(
        Member.id == member_id,
        Member.is_active == True
    ).first()
    
    if member:
        # Convert JSON strings back to Python objects for API responses
        if member.interests:
            try:
                member.interests = json.loads(member.interests)
            except json.JSONDecodeError:
                member.interests = None
        
        if member.skills:
            try:
                member.skills = json.loads(member.skills)
            except json.JSONDecodeError:
                member.skills = None
    
    return member


def update_member(db: Session, member_id: int, member_update: MemberUpdate) -> Optional[Member]:
    """Update a member's information"""
    db_member = db.query(Member).filter(
        Member.id == member_id,
        Member.is_active == True
    ).first()
    
    if not db_member:
        return None
    
    update_data = member_update.model_dump(exclude_unset=True)
    
    # Convert lists to JSON strings for database storage
    if 'interests' in update_data and update_data['interests'] is not None:
        update_data['interests'] = json.dumps(update_data['interests'])
    
    if 'skills' in update_data and update_data['skills'] is not None:
        update_data['skills'] = json.dumps(update_data['skills'])
    
    for field, value in update_data.items():
        setattr(db_member, field, value)
    
    db.commit()
    db.refresh(db_member)
    
    return get_member_by_id(db, member_id)


def delete_member(db: Session, member_id: int) -> bool:
    """Soft delete a member (set is_active to False)"""
    db_member = db.query(Member).filter(
        Member.id == member_id,
        Member.is_active == True
    ).first()
    
    if not db_member:
        return False
    
    db_member.is_active = False
    db.commit()
    return True


def get_member_options() -> dict:
    """Get predefined options for member interests and skills"""
    interests = [
        "Sports", "Soccer", "Basketball", "Baseball", "Tennis", "Swimming",
        "Music", "Piano", "Guitar", "Violin", "Singing", "Dancing",
        "Arts & Crafts", "Drawing", "Painting", "Sculpture", "Photography",
        "Science", "Robotics", "Chemistry", "Biology", "Astronomy",
        "Technology", "Coding", "Video Games", "Computer Graphics",
        "Reading", "Writing", "Poetry", "Storytelling",
        "Outdoor Activities", "Hiking", "Camping", "Fishing", "Gardening",
        "Board Games", "Puzzles", "Chess", "Card Games",
        "Drama", "Theater", "Acting", "Public Speaking",
        "Cooking", "Baking", "Martial Arts", "Yoga"
    ]
    
    skills = [
        "Swimming", "Cycling", "Running", "Jumping",
        "Piano Playing", "Guitar Playing", "Singing", "Dancing",
        "Drawing", "Painting", "Writing", "Reading",
        "Math", "Problem Solving", "Critical Thinking",
        "Communication", "Public Speaking", "Leadership",
        "Teamwork", "Organization", "Time Management",
        "Computer Skills", "Coding", "Typing",
        "Foreign Languages", "Spanish", "French", "Mandarin",
        "Soccer Skills", "Basketball Skills", "Baseball Skills",
        "Cooking", "Baking", "Gardening",
        "First Aid", "Safety Awareness",
        "Musical Instruments", "Art Techniques",
        "Creative Writing", "Research Skills"
    ]
    
    return {
        "interests": sorted(interests),
        "skills": sorted(skills)
    }