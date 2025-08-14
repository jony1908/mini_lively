#!/usr/bin/env python3
"""
Script to create a superuser for the admin dashboard
"""

import sys
import os
from passlib.context import CryptContext

# Add the current directory to Python path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal, init_db
from app.models.admin_user import AdminUser


def create_superuser(username: str, password: str):
    """Create a superuser with the given credentials"""
    
    # Initialize database (create tables if they don't exist)
    init_db()
    
    # Create password context for hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if superuser already exists
        existing_user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if existing_user:
            print(f"Admin user '{username}' already exists!")
            return False
        
        # Hash the password
        password_hash = pwd_context.hash(password)
        
        # Create new superuser
        superuser = AdminUser(
            username=username,
            password_hash=password_hash,
            is_superuser=True,
            is_active=True
        )
        
        # Add to database
        db.add(superuser)
        db.commit()
        
        print(f"Superuser '{username}' created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating superuser: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # Create the specified superuser
    username = "hfyz4@163.com"
    password = "1988hfyz"
    
    print("Creating superuser for admin dashboard...")
    success = create_superuser(username, password)
    
    if success:
        print(f"\n[SUCCESS] Superuser created!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("\nYou can now login to the admin dashboard at: http://localhost:8000/admin")
    else:
        print("\n[ERROR] Failed to create superuser")
        sys.exit(1)