import json
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from ..models.user_profile import UserProfile
from ..schemas.profile import UserProfileCreate, UserProfileUpdate


def get_user_profile(db: Session, user_id: int) -> Optional[UserProfile]:
    """Get user profile by user_id"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        # Convert JSON strings back to Python objects for API responses
        if profile.preferred_activity_types:
            try:
                profile.preferred_activity_types = json.loads(profile.preferred_activity_types)
            except json.JSONDecodeError:
                profile.preferred_activity_types = None
        
        if profile.preferred_schedule:
            try:
                profile.preferred_schedule = json.loads(profile.preferred_schedule)
            except json.JSONDecodeError:
                profile.preferred_schedule = None
                
        if profile.notification_preferences:
            try:
                profile.notification_preferences = json.loads(profile.notification_preferences)
            except json.JSONDecodeError:
                profile.notification_preferences = None
    
    return profile


def create_user_profile(db: Session, profile: UserProfileCreate, user_id: int) -> UserProfile:
    """Create a new user profile"""
    profile_data = profile.model_dump(exclude_unset=True)
    
    # Convert lists and dicts to JSON strings for database storage
    if 'preferred_activity_types' in profile_data and profile_data['preferred_activity_types']:
        profile_data['preferred_activity_types'] = json.dumps(profile_data['preferred_activity_types'])
    
    if 'preferred_schedule' in profile_data and profile_data['preferred_schedule']:
        profile_data['preferred_schedule'] = json.dumps(profile_data['preferred_schedule'])
        
    if 'notification_preferences' in profile_data and profile_data['notification_preferences']:
        profile_data['notification_preferences'] = json.dumps(profile_data['notification_preferences'])
    
    db_profile = UserProfile(**profile_data, user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return get_user_profile(db, user_id)


def update_user_profile(db: Session, user_id: int, profile_update: UserProfileUpdate) -> Optional[UserProfile]:
    """Update user profile"""
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not db_profile:
        return None
    
    update_data = profile_update.model_dump(exclude_unset=True)
    
    # Convert lists and dicts to JSON strings for database storage
    if 'preferred_activity_types' in update_data and update_data['preferred_activity_types'] is not None:
        update_data['preferred_activity_types'] = json.dumps(update_data['preferred_activity_types'])
    
    if 'preferred_schedule' in update_data and update_data['preferred_schedule'] is not None:
        update_data['preferred_schedule'] = json.dumps(update_data['preferred_schedule'])
        
    if 'notification_preferences' in update_data and update_data['notification_preferences'] is not None:
        update_data['notification_preferences'] = json.dumps(update_data['notification_preferences'])
    
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    
    return get_user_profile(db, user_id)


def delete_user_profile(db: Session, user_id: int) -> bool:
    """Delete user profile"""
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not db_profile:
        return False
    
    db.delete(db_profile)
    db.commit()
    return True