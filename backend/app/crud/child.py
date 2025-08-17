"""
Child CRUD operations.
Handles child profile management for authenticated users.
"""

import json
from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.child import Child
from ..schemas.child import ChildCreate, ChildUpdate


def create_child(db: Session, child: ChildCreate, parent_id: int) -> Child:
    """Create a new child profile for the authenticated user"""
    child_data = child.model_dump(exclude_unset=True)
    
    # Convert lists to JSON strings for database storage
    if 'interests' in child_data and child_data['interests']:
        child_data['interests'] = json.dumps(child_data['interests'])
    
    if 'skills' in child_data and child_data['skills']:
        child_data['skills'] = json.dumps(child_data['skills'])
    
    db_child = Child(**child_data, parent_id=parent_id)
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    
    return get_child_by_id(db, db_child.id, parent_id)


def get_user_children(db: Session, parent_id: int, active_only: bool = True) -> List[Child]:
    """Get all children for the authenticated user"""
    query = db.query(Child).filter(Child.parent_id == parent_id)
    
    if active_only:
        query = query.filter(Child.is_active == True)
    
    children = query.order_by(Child.created_at.desc()).all()
    
    # Convert JSON strings back to Python objects for API responses
    for child in children:
        if child.interests:
            try:
                child.interests = json.loads(child.interests)
            except json.JSONDecodeError:
                child.interests = None
        
        if child.skills:
            try:
                child.skills = json.loads(child.skills)
            except json.JSONDecodeError:
                child.skills = None
    
    return children


def get_child_by_id(db: Session, child_id: int, parent_id: int) -> Optional[Child]:
    """Get a specific child by ID, ensuring it belongs to the authenticated user"""
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.parent_id == parent_id,
        Child.is_active == True
    ).first()
    
    if child:
        # Convert JSON strings back to Python objects for API responses
        if child.interests:
            try:
                child.interests = json.loads(child.interests)
            except json.JSONDecodeError:
                child.interests = None
        
        if child.skills:
            try:
                child.skills = json.loads(child.skills)
            except json.JSONDecodeError:
                child.skills = None
    
    return child


def update_child(db: Session, child_id: int, parent_id: int, child_update: ChildUpdate) -> Optional[Child]:
    """Update a child's information"""
    db_child = db.query(Child).filter(
        Child.id == child_id,
        Child.parent_id == parent_id,
        Child.is_active == True
    ).first()
    
    if not db_child:
        return None
    
    update_data = child_update.model_dump(exclude_unset=True)
    
    # Convert lists to JSON strings for database storage
    if 'interests' in update_data and update_data['interests'] is not None:
        update_data['interests'] = json.dumps(update_data['interests'])
    
    if 'skills' in update_data and update_data['skills'] is not None:
        update_data['skills'] = json.dumps(update_data['skills'])
    
    for field, value in update_data.items():
        setattr(db_child, field, value)
    
    db.commit()
    db.refresh(db_child)
    
    return get_child_by_id(db, child_id, parent_id)


def delete_child(db: Session, child_id: int, parent_id: int) -> bool:
    """Soft delete a child (set is_active to False)"""
    db_child = db.query(Child).filter(
        Child.id == child_id,
        Child.parent_id == parent_id,
        Child.is_active == True
    ).first()
    
    if not db_child:
        return False
    
    db_child.is_active = False
    db.commit()
    return True


def get_child_options() -> dict:
    """Get predefined options for child interests and skills"""
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