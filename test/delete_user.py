#!/usr/bin/env python3
"""
Script to delete a user by email from the database
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.database.connection import get_db
from backend.app.crud.auth import AuthCRUD

def delete_user_by_email(email: str):
    """Delete user by email"""
    
    print(f"Attempting to delete user: {email}")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create AuthCRUD instance
        auth_crud = AuthCRUD(db)
        
        # Check if user exists first
        user = auth_crud.get_user_by_email(email)
        if not user:
            print(f"[INFO] User {email} not found in database")
            return False
            
        print(f"[INFO] Found user: {user.first_name} {user.last_name} (ID: {user.id})")
        print(f"[INFO] Verified: {user.is_verified}, Active: {user.is_active}")
        
        # Delete the user
        success = auth_crud.delete_user_by_email(email)
        
        if success:
            print(f"[SUCCESS] User {email} deleted successfully!")
            return True
        else:
            print(f"[ERROR] Failed to delete user {email}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error deleting user: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    target_email = "hfyz4@163.com"
    delete_user_by_email(target_email)