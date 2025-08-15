
# Backend Data Models

## Overview
This document describes the SQLAlchemy data models used in the Mini Lively backend system. All models inherit from the declarative base and use PostgreSQL as the underlying database.

## Base Model

### Base Class
**File**: `backend/app/models/base.py`

```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

All database models inherit from this `Base` class, which provides SQLAlchemy ORM functionality.

## User Model

### User Class
**File**: `backend/app/models/user.py`
**Table**: `users`

The User model represents parents and guardians who use the Mini Lively system to track their children's activities.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier for each user |
| `email` | String | Unique, Index, Not Null | User's email address for authentication |
| `password_hash` | String | Nullable | Hashed password (null for OAuth users) |
| `first_name` | String | Not Null | User's first name |
| `last_name` | String | Not Null | User's last name |
| `oauth_provider` | String | Nullable | OAuth provider ('google', 'apple', or null) |
| `oauth_id` | String | Nullable | External OAuth provider user ID |
| `created_at` | DateTime | Default: now | Account creation timestamp |
| `updated_at` | DateTime | Auto-update | Last modification timestamp |
| `is_active` | Boolean | Default: True | Account active status |
| `is_verified` | Boolean | Default: False | Email verification status |

#### Model Definition
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
```

#### Authentication Support
The User model supports two authentication methods:
1. **Email/Password**: Traditional registration with hashed password
2. **OAuth**: Google and Apple Sign-In integration

#### Key Features
- **Email Verification**: Users must verify their email before full access
- **OAuth Integration**: Seamless social login support
- **Flexible Authentication**: Supports both traditional and social authentication
- **Audit Trail**: Automatic timestamps for creation and updates
- **Account Status**: Active/inactive and verified status tracking

## Child Model

### Child Class
**File**: `backend/app/models/child.py`
**Table**: `children`

The Child model represents family members (children) being monitored in the Mini Lively system. Each child belongs to a parent (User) and contains detailed profile and activity information.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier for each child |
| `first_name` | String | Not Null | Child's first name |
| `last_name` | String | Not Null | Child's last name |
| `date_of_birth` | Date | Not Null | Child's birth date |
| `gender` | String | Nullable | Child's gender (optional) |
| `interests` | Text | Nullable | Child's interests and hobbies |
| `skills` | Text | Nullable | Child's current skills and abilities |
| `parent_id` | Integer | Foreign Key, Not Null | Reference to parent User |
| `created_at` | DateTime | Default: now | Record creation timestamp |
| `updated_at` | DateTime | Auto-update | Last modification timestamp |
| `is_active` | Boolean | Default: True | Child active status |

#### Computed Properties

| Property | Type | Description |
|----------|------|-------------|
| `age` | Integer | Current age calculated from date_of_birth |

#### Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| `parent` | Many-to-One | References User model (parent/guardian) |

#### Model Definition
```python
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .base import Base

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    
    # Relationships
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent = relationship("User", back_populates="children")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    @property
    def age(self) -> int:
        """Calculate and return the child's current age in years."""
        today = date.today()
        birth_date = self.date_of_birth
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
```

#### Key Features
- **Computed Age**: Automatic age calculation with proper handling of leap years and birthday timing
- **Parent Relationship**: Strong foreign key relationship with User model
- **Enhanced Profiles**: Support for interests, skills, and personal information
- **Admin Integration**: Full SQLAdmin interface with filtering, search, and form management
- **Data Integrity**: Proper constraints and validation rules

## Future Models

### Planned Models
- **Activity**: Individual activity records
- **Schedule**: Recurring activity schedules (hockey, art, etc.)
- **Event**: One-time events (birthday parties, etc.)
- **ActivityType**: Categories of activities
- **Location**: Activity locations

### Current Model Relationships
- User → Child (one-to-many) ✅ **Implemented**

### Future Model Relationships
- Child → Activity (one-to-many)
- User → Schedule (one-to-many)
- User → Event (one-to-many)

## Database Configuration

### Connection
Database connection is configured in `backend/app/database/connection.py` and uses environment variables for configuration.

### Migrations
The system uses SQLAlchemy's declarative approach for model definition. Database migrations should be managed through:
- SQLAlchemy metadata for table creation
- Version control for schema changes
- Environment-specific configurations

## Usage Examples

### Creating a User
```python
from app.models.user import User
from app.database.connection import get_db

# Email/password user
user = User(
    email="parent@example.com",
    password_hash=hash_password("secure_password"),
    first_name="Jane",
    last_name="Doe"
)

# OAuth user
oauth_user = User(
    email="parent@gmail.com",
    first_name="John",
    last_name="Smith",
    oauth_provider="google",
    oauth_id="google_user_12345",
    is_verified=True  # OAuth users are pre-verified
)
```

### Querying Users
```python
# Find user by email
user = session.query(User).filter(User.email == "parent@example.com").first()

# Get active, verified users
active_users = session.query(User).filter(
    User.is_active == True,
    User.is_verified == True
).all()
```
