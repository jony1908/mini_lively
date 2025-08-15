import pytest
from datetime import date, datetime
from app.models.child import Child
from app.models.user import User
from app.schemas.child import ChildCreate, ChildResponse, ChildUpdate


def test_child_model_creation():
    """Test that Child model can be instantiated with all fields"""
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


def test_child_model_minimal_creation():
    """Test that Child model can be created with minimal required fields"""
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


def test_child_schema_validation():
    """Test that Child schemas validate correctly"""
    # Test valid child creation
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


def test_child_schema_validation_future_date():
    """Test that Child schema rejects future birth dates"""
    with pytest.raises(ValueError, match="Date of birth cannot be in the future"):
        ChildCreate(
            first_name="Future",
            last_name="Child",
            date_of_birth=date(2030, 1, 1),
            parent_id=1
        )


def test_child_update_schema():
    """Test that Child update schema works correctly"""
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


def test_child_repr():
    """Test that Child model __repr__ works correctly"""
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


def test_child_age_calculation():
    """Test that Child age property calculates correctly"""
    today = date.today()
    
    # Test child born exactly 10 years ago
    ten_years_ago = date(today.year - 10, today.month, today.day)
    child = Child(
        first_name="Ten",
        last_name="Years",
        date_of_birth=ten_years_ago,
        parent_id=1
    )
    assert child.age == 10
    
    # Test child born 10 years and 1 day ago (should be 10)
    if today.day > 1:
        ten_years_one_day_ago = date(today.year - 10, today.month, today.day - 1)
    else:
        # Handle edge case for first day of month
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        ten_years_one_day_ago = date(prev_year - 10, prev_month, 28)
    
    child_older = Child(
        first_name="Older",
        last_name="Child",
        date_of_birth=ten_years_one_day_ago,
        parent_id=1
    )
    assert child_older.age == 10


def test_child_age_birthday_not_yet():
    """Test age calculation when birthday hasn't occurred this year"""
    today = date.today()
    
    # Create a future birthday this year
    if today.month < 12:
        future_birthday = date(today.year - 5, today.month + 1, today.day)
    else:
        future_birthday = date(today.year - 4, 1, today.day)
    
    child = Child(
        first_name="Future",
        last_name="Birthday",
        date_of_birth=future_birthday,
        parent_id=1
    )
    
    # If birthday hasn't occurred this year, age should be one less
    expected_age = today.year - future_birthday.year - 1
    assert child.age == expected_age


def test_child_age_birthday_today():
    """Test age calculation when today is the child's birthday"""
    today = date.today()
    birthday_5_years_ago = date(today.year - 5, today.month, today.day)
    
    child = Child(
        first_name="Birthday",
        last_name="Today",
        date_of_birth=birthday_5_years_ago,
        parent_id=1
    )
    
    assert child.age == 5


def test_child_age_leap_year():
    """Test age calculation with leap year considerations"""
    # Test a child born on February 29 (leap year)
    child = Child(
        first_name="Leap",
        last_name="Year",
        date_of_birth=date(2020, 2, 29),  # 2020 was a leap year
        parent_id=1
    )
    
    # Age should be calculated correctly regardless of current year being leap or not
    today = date.today()
    expected_age = today.year - 2020
    if (today.month, today.day) < (2, 29):
        expected_age -= 1
    
    assert child.age == expected_age


def test_child_age_newborn():
    """Test age calculation for very young children"""
    today = date.today()
    
    # Child born this year
    newborn = Child(
        first_name="New",
        last_name="Born",
        date_of_birth=today,
        parent_id=1
    )
    assert newborn.age == 0
    
    # Child born earlier this year
    if today.month > 1:
        earlier_this_year = date(today.year, 1, 1)
        child_this_year = Child(
            first_name="This",
            last_name="Year",
            date_of_birth=earlier_this_year,
            parent_id=1
        )
        assert child_this_year.age == 0


if __name__ == "__main__":
    # Run basic tests without database
    test_child_model_creation()
    test_child_model_minimal_creation()
    test_child_schema_validation()
    test_child_schema_validation_future_date()
    test_child_update_schema()
    test_child_repr()
    test_child_age_calculation()
    test_child_age_birthday_not_yet()
    test_child_age_birthday_today()
    test_child_age_leap_year()
    test_child_age_newborn()
    print("All Child model tests passed!")