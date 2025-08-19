#!/usr/bin/env python3
"""
Seed script to populate the database with default data.
Run this script to populate relationship_types table with default values.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.crud.relationship_type import seed_default_relationship_types

def main():
    """Seed the database with default data"""
    print("🌱 Starting database seeding...")
    
    db = SessionLocal()
    try:
        # Seed relationship types
        created_types = seed_default_relationship_types(db)
        
        if created_types:
            print(f"✅ Created {len(created_types)} relationship types:")
            for rel_type in created_types:
                print(f"   - {rel_type.display_name} ({rel_type.name})")
        else:
            print("ℹ️ All relationship types already exist")
            
        print("🎉 Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        return 1
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)