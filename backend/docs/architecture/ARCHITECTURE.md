# Mini Lively Backend Architecture

## Project Overview
A FastAPI-based family activity monitoring system that allows parents and guardians to track their children's daily activities, manage schedules for recurring activities (like hockey, art, soccer classes), and organize events (like birthday parties).

## Project Structure
```
├── app  # Contains the main application files.
│   ├── __init__.py   # this file makes "app" a "Python package"
│   ├── main.py       # Initializes the FastAPI application.
│   ├── dependencies.py # Defines dependencies used by the routers
│   ├── routers
│   │   ├── __init__.py
│   │   ├── users.py        # User management endpoints
│   ├── crud
│   │   ├── __init__.py
│   │   ├── user.py             # User CRUD operations
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   ├── models
│   │   ├── __init__.py
│   │   ├── base.py             # Base SQLAlchemy model
│   │   ├── user.py             # User database model
│   ├── external_services
│   │   ├── __init__.py
│   │   ├── email.py          # Email notification services
│   │   └── notification.py   # Push notification services
│   └── utils
│       ├── __init__.py
│       ├── authentication.py  # Authentication utilities
│       └── validation.py      # Data validation utilities
├── tests
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_users.py       # User endpoint tests
├── requirements.txt
├── .gitignore
├── README.md
└── CLAUDE.md
```

## Architecture Components

### **Core Models**
- **User**: Parents/guardians who manage children's activities

### **API Layer Structure**
- **REST API**: Built with FastAPI for high performance
- **Router-based Organization**: Each domain has its own router module
- **Dependency Injection**: Database sessions and authentication
- **Automatic Documentation**: OpenAPI/Swagger integration