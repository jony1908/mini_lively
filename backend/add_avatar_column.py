#!/usr/bin/env python3
"""
Migration script to add avatar_url column to children table.
Run this script to add the missing avatar_url column to the existing children table.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import text
from app.database.connection import engine
from app.config.settings import settings

def add_avatar_column():
    """Add avatar_url column to children table if it doesn't exist."""
    try:
        with engine.connect() as connection:
            # Check if column already exists
            check_column_sql = """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'children' AND column_name = 'avatar_url';
            """
            
            result = connection.execute(text(check_column_sql))
            column_exists = result.fetchone()
            
            if column_exists:
                print("Column 'avatar_url' already exists in 'children' table")
                return
            
            # Add the column
            add_column_sql = """
            ALTER TABLE children 
            ADD COLUMN avatar_url VARCHAR NULL;
            """
            
            connection.execute(text(add_column_sql))
            connection.commit()
            
            print("Successfully added 'avatar_url' column to 'children' table")
            
    except Exception as e:
        print(f"Error adding avatar_url column: {str(e)}")
        sys.exit(1)

def verify_column():
    """Verify that the column was added successfully."""
    try:
        with engine.connect() as connection:
            # Check column details
            column_info_sql = """
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'children' AND column_name = 'avatar_url';
            """
            
            result = connection.execute(text(column_info_sql))
            column_info = result.fetchone()
            
            if column_info:
                print(f"Column verification successful:")
                print(f"   - Name: {column_info[0]}")
                print(f"   - Type: {column_info[1]}")
                print(f"   - Nullable: {column_info[2]}")
            else:
                print("Column verification failed - column not found")
                
    except Exception as e:
        print(f"Error verifying column: {str(e)}")

if __name__ == "__main__":
    print("Starting migration to add avatar_url column to children table...")
    print(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Local database'}")
    
    add_avatar_column()
    verify_column()
    
    print("Migration completed successfully!")