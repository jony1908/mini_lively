# Mini Lively Backend

## Project Overview
A FastAPI backend with PostgreSQL database, featuring modular API endpoints routed to different data tables. The backend provides authentication, user management, and activity tracking capabilities for the Mini Lively family activity monitoring system.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Validation**: Pydantic
- **Testing**: pytest
- **Admin**: sqladmin

## Key Features
- JWT-based authentication system
- Modular API design with separate routers
- Database models for users and activities
- Email service integration
- Admin dashboard with SQLAdmin
- Comprehensive test coverage

## Architecture References

### Core Architecture
- **System Architecture**: `docs/backend/architecture/ARCHITECTURE.md`
- **Data Models**: `docs/backend/architecture/MODELS.md`
- **Database Schema**: `docs/backend/architecture/DATABASE_SCHEMA.md`
- **API Endpoints**: `docs/backend/architecture/API_ENDPOINT.md`
- **Backend Admin**: `docs/backend/architecture/ADMIN.md`

### Development Resources
- **Setup Guide**: `docs/backend/development/SETUP.md`
- **Development Commands**: `docs/backend/development/COMMAND.md`
- **Coding Standards**: `docs/backend/development/CODING.md`
- **Testing Guide**: `docs/backend/development/TESTING.md`

## Admin Dashboard

The backend includes a web-based admin dashboard powered by SQLAdmin for managing database records:

- **URL**: `http://localhost:8000/admin`
- **Authentication**: Secure login with database-stored admin users
- **Features**: 
  - User management (view, edit, delete users)
  - Admin user management
  - Search and filter capabilities
  - Pagination for large datasets
  - Responsive web interface

### Admin Access
- **Primary Superuser**: `hfyz4@163.com` / `1988hfyz`
- **Fallback Admin**: Configurable via `ADMIN_USERNAME` and `ADMIN_PASSWORD` environment variables

### Admin Configuration
Admin settings are located in:
- `backend/app/admin/config.py` - Authentication backend and admin setup
- `backend/app/admin/views.py` - Model views and configurations
- `backend/app/admin/README.md` - Detailed admin documentation

## Important References

For detailed development setup, commands, and API documentation, see the development and architecture documentation.