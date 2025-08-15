#!/usr/bin/env python3
"""
Simple test to verify Child model and schemas work correctly
without external dependencies
"""

import sys
import os
from datetime import date, datetime

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.child import Child
from app.models.user import User
from app.schemas.child import ChildCreate, ChildResponse, ChildUpdate


def test_child_model_creation():
    """Test that Child model can be instantiated with all fields"""
    print("Testing Child model creation...")
    
    child = Child(
        first_name="Emma",
        last_name="Johnson",
        date_of_birth=date(2015, 6, 15),
        gender="female",
        interests="soccer, art, reading",
        skills="beginner swimming, intermediate reading",
        parent_id=1,
        is_active=True  # Explicitly set default value for testing
    )
    
    assert child.first_name == "Emma"
    assert child.last_name == "Johnson"
    assert child.date_of_birth == date(2015, 6, 15)
    assert child.gender == "female"
    assert child.interests == "soccer, art, reading"
    assert child.skills == "beginner swimming, intermediate reading"
    assert child.parent_id == 1
    assert child.is_active is True
    print("✓ Child model creation test passed")


def test_child_model_minimal():
    """Test that Child model can be created with minimal required fields"""
    print("Testing Child model minimal creation...")
    
    child = Child(
        first_name="Alex",
        last_name="Smith",
        date_of_birth=date(2012, 3, 22),
        parent_id=2,
        is_active=True  # Explicitly set default value for testing
    )
    
    assert child.first_name == "Alex"
    assert child.last_name == "Smith"
    assert child.date_of_birth == date(2012, 3, 22)
    assert child.gender is None
    assert child.interests is None
    assert child.skills is None
    assert child.parent_id == 2
    assert child.is_active is True
    print("✓ Child model minimal creation test passed")


def test_child_schema_validation():
    """Test that Child schemas validate correctly"""
    print("Testing Child schema validation...")
    
    child_data = {
        "first_name": "Sophie",
        "last_name": "Brown",
        "date_of_birth": date(2014, 9, 10),
        "gender": "female",
        "interests": "dancing, painting",
        "skills": "beginner ballet, intermediate painting",
        "parent_id": 3
    }
    
    child_create = ChildCreate(**child_data)
    assert child_create.first_name == "Sophie"
    assert child_create.interests == "dancing, painting"
    assert child_create.skills == "beginner ballet, intermediate painting"
    print("✓ Child schema validation test passed")


def test_child_schema_future_date():
    """Test that Child schema rejects future birth dates"""
    print("Testing Child schema future date validation...")
    
    try:
        ChildCreate(
            first_name="Future",
            last_name="Child",
            date_of_birth=date(2030, 1, 1),
            parent_id=1
        )
        assert False, "Should have raised ValueError for future date"
    except ValueError as e:
        assert "Date of birth cannot be in the future" in str(e)
        print("✓ Child schema future date validation test passed")


def test_child_update_schema():
    """Test that Child update schema works correctly"""
    print("Testing Child update schema...")
    
    update_data = {
        "interests": "soccer, music, coding",
        "skills": "intermediate soccer, beginner guitar",
        "is_active": True
    }
    
    child_update = ChildUpdate(**update_data)
    assert child_update.interests == "soccer, music, coding"
    assert child_update.skills == "intermediate soccer, beginner guitar"
    assert child_update.is_active is True
    assert child_update.first_name is None  # Not updated
    print("✓ Child update schema test passed")


def test_child_repr():
    """Test that Child model __repr__ works correctly"""
    print("Testing Child model __repr__...")
    
    child = Child(
        first_name="Test",
        last_name="Child",
        date_of_birth=date(2010, 1, 1),
        parent_id=999
    )
    child.id = 123
    
    repr_str = repr(child)
    assert "Child" in repr_str
    assert "id=123" in repr_str
    assert "name='Test Child'" in repr_str
    assert "age=" in repr_str
    assert "parent_id=999" in repr_str
    print("✓ Child model __repr__ test passed")


def test_child_age_property():
    """Test that Child age property works correctly"""
    print("Testing Child age property...")
    
    today = date.today()
    
    # Test a 10-year-old child
    ten_years_ago = date(today.year - 10, today.month, today.day)
    child = Child(
        first_name="Ten",
        last_name="Years",
        date_of_birth=ten_years_ago,
        parent_id=1
    )
    
    assert child.age == 10
    print(f"✓ Child age calculation test passed (age: {child.age})")
    
    # Test a newborn
    newborn = Child(
        first_name="New",
        last_name="Born",
        date_of_birth=today,
        parent_id=1
    )
    
    assert newborn.age == 0
    print(f"✓ Newborn age calculation test passed (age: {newborn.age})")


def test_user_child_relationship():
    """Test that User model has children relationship"""
    print("Testing User-Child relationship...")
    
    user = User(
        email="parent@example.com",
        first_name="Jane",
        last_name="Doe"
    )
    
    # Check that the children relationship exists
    assert hasattr(user, 'children')
    print("✓ User-Child relationship test passed")


if __name__ == "__main__":
    print("Running Child model tests...\n")
    
    try:
        test_child_model_creation()
        test_child_model_minimal()
        test_child_schema_validation()
        test_child_schema_future_date()
        test_child_update_schema()
        test_child_repr()
        test_child_age_property()
        test_user_child_relationship()
        
        print("\n✓ All Child model tests passed successfully!")
        print("\nChild model features tested:")
        print("- Enhanced fields: interests and skills")
        print("- Required fields: first_name, last_name, date_of_birth, parent_id")
        print("- Optional fields: gender, interests, skills")
        print("- Age calculation: computed property based on date_of_birth")
        print("- Schema validation including future date rejection")
        print("- Update schemas for partial updates")
        print("- User-Child relationship")
        
    except Exception as e:
        print(f"\nX Test failed: {e}")
        sys.exit(1)