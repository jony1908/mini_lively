
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
| `first_name` | String | Nullable | User's first name (optional) |
| `last_name` | String | Nullable | User's last name (optional) |
| `oauth_provider` | String | Nullable | OAuth provider ('google', 'apple', or null) |
| `oauth_id` | String | Nullable | External OAuth provider user ID |
| `created_at` | DateTime | Default: now | Account creation timestamp |
| `updated_at` | DateTime | Auto-update | Last modification timestamp |
| `is_active` | Boolean | Default: True | Account active status |
| `is_verified` | Boolean | Default: False | Email verification status |

#### Model Definition
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        name_part = f"{self.first_name or ''} {self.last_name or ''}".strip() or "No Name"
        return f"<User(id={self.id}, email='{self.email}', name='{name_part}')>"
    
    def __str__(self):
        name_part = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return f"{name_part} ({self.email})" if name_part else self.email
```

#### Authentication Support
The User model supports two authentication methods:
1. **Email/Password**: Traditional registration with hashed password
2. **OAuth**: Google and Apple Sign-In integration

#### Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| `profile` | One-to-One | References UserProfile model (additional user data) |

#### String Representation
The User model includes enhanced string representation for better debugging and admin display:
- **`__repr__`**: `<User(id=13, email='user@example.com', name='John Doe')>` or `<User(id=13, email='user@example.com', name='No Name')>`
- **`__str__`**: `John Doe (user@example.com)` or `user@example.com` (if no name provided)

#### Key Features
- **Email Verification**: Users must verify their email before full access
- **OAuth Integration**: Seamless social login support
- **Flexible Authentication**: Supports both traditional and social authentication
- **Audit Trail**: Automatic timestamps for creation and updates
- **Account Status**: Active/inactive and verified status tracking
- **Profile Support**: Optional extended profile information via UserProfile relationship

## UserProfile Model

### UserProfile Class
**File**: `backend/app/models/user_profile.py`
**Table**: `user_profiles`

The UserProfile model stores extended profile information for users in the Mini Lively system. This model provides additional contact, location, and preference data that supports activity management and regional features.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier for each profile |
| `phone_number` | String | Nullable | Primary contact phone number |
| `profile_picture_url` | String | Nullable | URL/path to profile image |
| `city` | String | Nullable | User's city |
| `state` | String | Nullable | User's state/province |
| `postal_code` | String | Nullable, Index | Zip/postal code for regional searches |
| `country` | String | Nullable | User's country |
| `timezone` | String | Nullable | User's timezone for scheduling |
| `preferred_activity_types` | Text | Nullable | JSON string of activity preferences |
| `preferred_schedule` | Text | Nullable | JSON string of availability preferences |
| `notification_preferences` | Text | Nullable | JSON string of communication preferences |
| `user_id` | Integer | Foreign Key, Unique, Not Null | Reference to parent User |
| `created_at` | DateTime | Default: now | Profile creation timestamp |
| `updated_at` | DateTime | Auto-update | Last modification timestamp |

#### Relationships

| Relationship | Type | Description |
|--------------|------|-------------|
| `user` | One-to-One | References User model (profile owner) |

#### Model Definition
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Contact Information
    phone_number = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    
    # Location
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True, index=True)
    country = Column(String, nullable=True)
    
    # Activity Preferences (stored as JSON strings)
    preferred_activity_types = Column(Text, nullable=True)
    preferred_schedule = Column(Text, nullable=True)
    
    # Settings
    timezone = Column(String, nullable=True)
    notification_preferences = Column(Text, nullable=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User", back_populates="profile")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### JSON Field Structure
The UserProfile model uses JSON-stored text fields for flexible preference management:

**`preferred_activity_types`** (List of strings):
```json
["sports", "arts", "music", "outdoors"]
```

**`preferred_schedule`** (Schedule preferences):
```json
{
  "weekdays": ["monday", "wednesday", "friday"],
  "times": ["morning", "afternoon"],
  "duration": "1-2 hours"
}
```

**`notification_preferences`** (Communication settings):
```json
{
  "email": true,
  "sms": false,
  "push": true,
  "frequency": "daily"
}
```

#### Key Features
- **Geographic Indexing**: Postal code field indexed for fast regional searches
- **Flexible Preferences**: JSON-based storage for extensible activity and schedule preferences
- **One-to-One Relationship**: Each user can have exactly one profile
- **Optional Data**: All fields nullable for gradual profile completion
- **Activity Management**: Support for location-based activity discovery
- **Communication Control**: Granular notification preference management

#### Regional Features
- **Postal Code Search**: Fast lookup for activities in user's area
- **Geographic Filtering**: Filter users by city, state, country, postal code
- **Timezone Support**: Schedule activities across different time zones
- **Location Analytics**: Regional user distribution and activity patterns

## Member Model

### Member Class
**File**: `backend/app/models/member.py`
**Table**: `member`

The memeber model represents family members (children, userself, spounse, etc) being monitored in the Mini Lively system.

#### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Index | Unique identifier for each member |
| `first_name` | String | Not Null | Member's first name |
| `last_name` | String | Not Null | Member's last name |
| `date_of_birth` | Date | Not Null | Member's birth date |
| `gender` | String | Nullable | Member's gender (optional) |
| `interests` | Text | Nullable | Member's interests and hobbies |
| `skills` | Text | Nullable | Member's current skills and abilities |
| `created_at` | DateTime | Default: now | Record creation timestamp |
| `updated_at` | DateTime | Auto-update | Last modification timestamp |
| `is_active` | Boolean | Default: True | Member active status |

#### Computed Properties

| Property | Type | Description |
|----------|------|-------------|
| `age` | Integer | Current age calculated from date_of_birth |


#### Model Definition
```python
from sqlalchemy import Column, Integer, String, Date, Text, DateTime, Boolean
from datetime import datetime, date
from .base import Base

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=True)
    
    # Enhanced profile fields
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    @property
    def age(self) -> int:
        """Calculate and return the member's current age in years."""
        today = date.today()
        birth_date = self.date_of_birth
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    
    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.first_name} {self.last_name}', age={self.age})>"
```

## Database Configuration

### Connection
Database connection is configured in `backend/app/database/connection.py` and uses environment variables for configuration.

### Migrations
The system uses SQLAlchemy's declarative approach for model definition. Database migrations should be managed through:
- SQLAlchemy metadata for table creation
- Version control for schema changes
- Environment-specific configurations