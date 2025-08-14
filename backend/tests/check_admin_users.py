#!/usr/bin/env python3
"""
Script to check admin users in the database
"""

import sys
import os

# Add the current directory to Python path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.models.admin_user import AdminUser


def check_admin_users():
    """Check all admin users in the database"""
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Query all admin users
        admin_users = db.query(AdminUser).all()
        
        if not admin_users:
            print("No admin users found in the database.")
            return
        
        print(f"Found {len(admin_users)} admin user(s):")
        print("-" * 60)
        
        for user in admin_users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Is Superuser: {user.is_superuser}")
            print(f"Is Active: {user.is_active}")
            print(f"Created: {user.created_at}")
            print(f"Updated: {user.updated_at}")
            print("-" * 60)
        
    except Exception as e:
        print(f"Error checking admin users: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    check_admin_users()