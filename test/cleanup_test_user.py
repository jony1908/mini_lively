#!/usr/bin/env python3
"""
Cleanup script to delete test user
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.database.connection import get_db
from backend.app.crud.auth import AuthCRUD

def cleanup_test_user():
    """Delete test user if exists"""
    test_email = "test_verification@example.com"
    
    try:
        db = next(get_db())
        auth_crud = AuthCRUD(db)
        
        user = auth_crud.get_user_by_email(test_email)
        if user:
            success = auth_crud.delete_user_by_email(test_email)
            if success:
                print(f"[OK] Test user {test_email} deleted successfully")
            else:
                print(f"[ERROR] Failed to delete test user {test_email}")
        else:
            print(f"[INFO] Test user {test_email} not found")
            
    except Exception as e:
        print(f"[ERROR] Cleanup failed: {str(e)}")
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    cleanup_test_user()