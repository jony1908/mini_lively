#!/usr/bin/env python3
"""
Script to create test data for Child model
"""

import sys
import os
from datetime import date

# Add the current directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal, init_db
from app.models.user import User
from app.models.child import Child


def create_test_data():
    """Create test users and children for testing admin interface"""
    print("Creating test data...")
    
    # Initialize database
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if we already have test data
        existing_users = db.query(User).filter(User.email.like('%test%')).count()
        if existing_users > 0:
            print(f"Found {existing_users} existing test users. Skipping user creation.")
        else:
            # Create test users
            test_users = [
                User(
                    email="parent1@test.com",
                    first_name="John",
                    last_name="Doe",
                    is_active=True,
                    is_verified=True
                ),
                User(
                    email="parent2@test.com", 
                    first_name="Jane",
                    last_name="Smith",
                    is_active=True,
                    is_verified=True
                ),
                User(
                    email="parent3@test.com",
                    first_name="Mike",
                    last_name="Johnson",
                    is_active=True,
                    is_verified=True
                )
            ]
            
            for user in test_users:
                db.add(user)
            
            db.commit()
            print("+ Created 3 test users")
        
        # Get all users for creating children
        users = db.query(User).all()
        if len(users) == 0:
            print("X No users found in database. Cannot create children.")
            return
        
        # Check if we already have test children
        existing_children = db.query(Child).count()
        if existing_children > 0:
            print(f"Found {existing_children} existing children. Skipping child creation.")
        else:
            # Create test children
            test_children = [
                Child(
                    first_name="Emma",
                    last_name="Doe",
                    date_of_birth=date(2015, 6, 15),
                    gender="female",
                    interests="soccer, art, reading",
                    skills="beginner swimming, intermediate reading",
                    parent_id=users[0].id,
                    is_active=True
                ),
                Child(
                    first_name="Alex",
                    last_name="Doe", 
                    date_of_birth=date(2012, 3, 22),
                    gender="male",
                    interests="basketball, video games",
                    skills="intermediate basketball, beginner guitar",
                    parent_id=users[0].id,
                    is_active=True
                ),
                Child(
                    first_name="Sophie",
                    last_name="Smith",
                    date_of_birth=date(2014, 9, 10),
                    gender="female", 
                    interests="dancing, painting",
                    skills="beginner ballet, intermediate painting",
                    parent_id=users[1].id if len(users) > 1 else users[0].id,
                    is_active=True
                ),
                Child(
                    first_name="Lucas",
                    last_name="Johnson",
                    date_of_birth=date(2016, 12, 5),
                    gender="male",
                    interests="science, robots",
                    skills="beginner coding, intermediate science",
                    parent_id=users[2].id if len(users) > 2 else users[0].id,
                    is_active=True
                ),
                Child(
                    first_name="Mia",
                    last_name="Johnson",
                    date_of_birth=date(2018, 4, 20),
                    gender="female",
                    interests="music, animals",
                    skills="beginner piano, animal care",
                    parent_id=users[2].id if len(users) > 2 else users[0].id,
                    is_active=True
                )
            ]
            
            for child in test_children:
                db.add(child)
            
            db.commit()
            print("+ Created 5 test children")
        
        # Show summary
        total_users = db.query(User).count()
        total_children = db.query(Child).count()
        print(f"\nDatabase Summary:")
        print(f"- Total Users: {total_users}")
        print(f"- Total Children: {total_children}")
        
        # Show some sample data
        print(f"\nSample Children:")
        children = db.query(Child).limit(3).all()
        for child in children:
            print(f"- {child.first_name} {child.last_name}, Age: {child.age}, Parent: {child.parent.email}")
        
        print("\n+ Test data creation completed successfully!")
        
    except Exception as e:
        print(f"X Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()