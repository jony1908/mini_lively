# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mini Lively is a full-stack family activity monitoring system with a FastAPI backend and React frontend. It allows parents to track children's activities, manage recurring schedules (hockey, art, soccer), and organize events (birthday parties).

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
- **API Routers**: Domain-specific endpoints in `app/routers/` (users, children, activities, events, schedules, attendances, dashboard)
- **CRUD Operations**: Data access layer in `app/crud/`
- **Schemas**: Pydantic models for API validation in `app/schemas/`
- **External Services**: Email and notification services in `app/external_services/`

### Frontend Structure
- **React 19 + Vite**: Modern React with fast development server
- **Component Structure**: Reusable components in `src/components/`
- **Page Components**: Route-level components in `src/pages/`
- **Styling**: CSS modules approach with component-specific CSS files

### Key Integrations
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated at http://localhost:8000/docs
- **CORS**: Enabled for frontend-backend communication
- **Testing**: pytest for backend, FastAPI TestClient for API tests

## Important File Locations

### Backend Documentation
- **Architecture Details**: `backend/docs/architecture/ARCHITECTURE.md`
- **Database Schema**: `backend/docs/architecture/DATABASE_SCHEMA.md`
- **API Endpoints**: `backend/docs/architecture/API_ENDPOINT.md`
- **Setup Instructions**: `backend/docs/development/SETUP.md`
- **Development Commands**: `backend/docs/development/COMMAND.md`

### Frontend Documentation
- **Architecture**: `frontend/docs/architecture/ARCHITECTURE.md`

## Development Workflow

1. **Backend Development**: Work in `backend/` directory, use `python -m app.main` to start server
2. **Frontend Development**: Work in `frontend/` directory, use `npm run dev` for development
3. **Testing**: Run `pytest` in backend directory for API tests
4. **API Testing**: Use http://localhost:8000/docs for interactive API documentation

## All the Summary and Update .md files should go to './summary' folder