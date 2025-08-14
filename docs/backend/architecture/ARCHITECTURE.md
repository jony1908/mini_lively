# Mini Lively Backend Architecture

## Overview
A FastAPI-based family activity monitoring system that allows parents and guardians to track their children's daily activities, manage schedules for recurring activities (like hockey, art, soccer classes), and organize events (like birthday parties).

## Technology Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Validation**: Pydantic
- **Testing**: pytest

## Application Architecture

### Project Structure
```
backend/
├── app/
│   ├── config/         # Configuration settings
│   │   ├── __init__.py
│   │   └── settings.py # Environment and app settings
│   ├── crud/           # CRUD operations
│   │   ├── __init__.py
│   │   └── auth.py     # Authentication CRUD operations
│   ├── database/       # Database connection
│   │   ├── __init__.py
│   │   └── connection.py # Database setup and connection
│   ├── models/         # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py     # Base SQLAlchemy model
│   │   └── user.py     # User database model
│   ├── routers/        # API route handlers
│   │   ├── __init__.py
│   │   └── auth.py     # Authentication endpoints
│   ├── schemas/        # Pydantic schemas
│   │   ├── __init__.py
│   │   └── auth.py     # Authentication request/response schemas
│   ├── utils/          # Utility functions
│   │   ├── __init__.py
│   │   ├── auth.py     # Authentication utilities
│   │   └── email_service.py # Email service utilities
│   └── main.py         # FastAPI application entry point
├── tests/              # Test files
│   ├── __init__.py
│   ├── test_main.py    # Main application tests
│   ├── test_posts.py   # Post-related tests
│   └── test_users.py   # User-related tests
└── requirements.txt    # Python dependencies
```

## Architecture Components

### Core Models
- **User**: Parents/guardians who manage children's activities
- Extensible design for future activity and event models

### API Layer Structure
- **REST API**: Built with FastAPI for high performance and automatic documentation
- **Router-based Organization**: Each domain (auth, users, activities) has its own router module
- **Dependency Injection**: Database sessions, authentication, and configuration
- **Automatic Documentation**: OpenAPI/Swagger integration at `/docs` and `/redoc`

### Key Features
- **JWT-based Authentication**: Secure token-based authentication system
- **Modular Design**: Separate routers for different functional areas
- **Database Integration**: SQLAlchemy ORM with PostgreSQL
- **Email Services**: Integrated email service for notifications
- **Comprehensive Testing**: pytest-based test suite

### Authentication Flow
1. User registration with email verification
2. JWT token generation upon login
3. Token-based authentication for protected endpoints
4. Refresh token mechanism for session management

### API Documentation
Once running, interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Development Architecture
- **Environment-based Configuration**: Settings managed through environment variables
- **Database Migrations**: SQLAlchemy-based model management
- **Testing Strategy**: Unit and integration tests with pytest
- **Code Organization**: Clean separation of concerns across modules