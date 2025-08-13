# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mini Lively is a full-stack family activity monitoring system with a FastAPI backend and React frontend. It allows parents to track children's activities, manage recurring schedules (hockey, art, soccer), and organize events (birthday parties).

**Current Status**: ✅ User authentication module is fully implemented with email/password login, Google/Apple OAuth, and email verification.

## Development Commands

### Backend (FastAPI + PostgreSQL)
- `cd backend` to navigate to backend directory
- `pip install -r requirements.txt` - Install Python dependencies
- `python -m app.main` - Start development server on http://localhost:8000
- `pytest` - Run backend tests
- `pytest tests/test_main.py` - Run specific test file

### Frontend (React + Vite)
- `cd frontend` to navigate to frontend directory
- `npm install` - Install dependencies
- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## Architecture Overview

### Backend Structure
- **FastAPI Application**: Modular router-based organization in `backend/app/`
- **Database Models**: SQLAlchemy models in `app/models/` (User, Child, Activity, Event, etc.)
- **API Routers**: Domain-specific endpoints in `app/routers/` (auth, users, children, activities, events, schedules, attendances, dashboard)
- **CRUD Operations**: Data access layer in `app/crud/`
- **Schemas**: Pydantic models for API validation in `app/schemas/`
- **Authentication**: JWT-based auth with OAuth support in `app/auth.py`
- **Email Services**: Email verification and notifications in `app/email_service.py`

### Frontend Structure
- **React 19 + Vite**: Modern React with fast development server
- **Component Structure**: Reusable components in `src/components/`
- **Services**: API services in `src/services/` (renamed from api/)
- **Contexts**: React Context for state management in `src/contexts/`
- **Styling**: Tailwind CSS with design-matching components

### Key Integrations
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with refresh mechanism
- **OAuth**: Google and Apple OAuth integration ready
- **Email**: SMTP-based email verification system
- **API Documentation**: Auto-generated at http://localhost:8000/docs
- **CORS**: Enabled for frontend-backend communication
- **Testing**: pytest for backend, FastAPI TestClient for API tests

## Authentication System

### Backend Components
- **User Model**: `app/models/user.py` - SQLAlchemy model with auth fields
- **Auth Utilities**: `app/auth.py` - Password hashing, JWT tokens, OAuth utils
- **Auth CRUD**: `app/crud/auth.py` - Database operations for users
- **Auth Router**: `app/routers/auth.py` - API endpoints for authentication
- **Auth Schemas**: `app/schemas/auth.py` - Pydantic models for validation
- **Email Service**: `app/email_service.py` - Email verification system

### Frontend Components
- **Auth Context**: `src/contexts/AuthContext.jsx` - Global auth state management
- **Auth Services**: `src/services/auth.js` - API calls for authentication
- **API Client**: `src/services/client.js` - Axios client with interceptors
- **Login Component**: `src/components/Login.jsx` - Design-matching login form
- **Register Component**: `src/components/Register.jsx` - Design-matching registration form
- **Email Verification**: `src/components/EmailVerification.jsx` - Email verification page
- **Protected Routes**: `src/components/ProtectedRoute.jsx` - Route authentication guard

## Important File Locations

### Backend Documentation
- **Backend Details**: `backend/CLAUDE.md`
- **Architecture Details**: `backend/docs/architecture/ARCHITECTURE.md`
- **Database Schema**: `backend/docs/architecture/DATABASE_SCHEMA.md`
- **API Endpoints**: `backend/docs/architecture/API_ENDPOINT.md`
- **Setup Instructions**: `backend/docs/development/SETUP.md`
- **Development Commands**: `backend/docs/development/COMMAND.md`

### Frontend Documentation
- **Frontend Details**: `frontend/CLAUDE.md`
- **Architecture**: `frontend/docs/architecture/ARCHITECTURE.md`
- **Design Files**: `frontend/design/` - Original HTML design mockups

## Development Workflow

1. **Backend Development**: Work in `backend/` directory, use `python -m app.main` to start server
2. **Frontend Development**: Work in `frontend/` directory, use `npm run dev` for development
3. **Authentication Testing**: Create account, verify email, test login/logout flows
4. **API Testing**: Use http://localhost:8000/docs for interactive API documentation
5. **Database**: Users are stored with proper authentication fields and email verification status

## Current Features

### ✅ Implemented
- **User Registration**: Email/password with verification email
- **User Login**: Email/password authentication
- **Email Verification**: SMTP-based verification with beautiful HTML emails
- **JWT Authentication**: Access and refresh token system
- **OAuth Ready**: Google and Apple OAuth integration configured
- **Protected Routes**: Frontend route guards and authentication state
- **Design Compliance**: Components match provided HTML designs exactly
- **Password Security**: Bcrypt hashing with proper salt rounds
- **Auto Token Refresh**: Seamless token renewal in frontend
- **Error Handling**: Comprehensive error messages and user feedback

### 🚧 Next Features to Implement
- Child profile management
- Activity tracking and scheduling
- Event organization and attendance
- Dashboard with family activity overview
- Notification system for upcoming activities

## All the Summary and Update .md files should go to './summary' folder