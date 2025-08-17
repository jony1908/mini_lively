# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mini Lively is a full-stack family activity monitoring system with a FastAPI backend and React frontend. It allows parents to track children's activities, manage recurring schedules (hockey, art, soccer), and organize events (birthday parties). 

The full documents for the project is under 'docs/' fodler. Read comprehensively thru all the reference files with thd folder for both backend and frontend and think hard to build the best practice according 
to the requriements.

## Architecture Overview

### Backend (FastAPI + PostgreSQL)
- Location: `backend/`
- Main entry: `backend/app/main.py`
- Modular API endpoints with separate routers
- Authentication system with JWT tokens
- Database models using SQLAlchemy
- virtual env: `venv/` #all the installment needs go to side

### Frontend (React + Vite)
- Location: `frontend/`
- Main entry: `frontend/src/main.jsx`
- Mobile-first responsive design
- Context-based state management
- Authentication integration

## Important File Locations

### Backend Documentation
- **Backend Overview**: `docs/backend/BACKEND.md`

### Frontend Documentation  
- **Frontend Overview**: `docs/frontend/FRONTEND.md`

### Project Roadmap
- **Development Roadmap**: `docs/summary/ROADMAP.md`

## Documentation Structure

### Backend References
- **Architecture**: `docs/backend/architecture/`
- **Development**: `docs/backend/development/`

### Frontend References
- **Architecture**: `docs/frontend/architecture/`
- **Development**: `docs/frontend/development/`

### Summary Documents
- **Progress Summary**: `docs/summary/`
- **CURRENT TASK**: `docs/summary/CURRENT_TASK.md`

### Test Documents
- **Location**: `test/`

## Key Technologies
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, JWT, Pydantic
- **Frontend**: React, Vite, Tailwind CSS, Context API
- **Authentication**: JWT tokens with refresh mechanism

## Coding Standard
- Add consice comments for each module and complex functions.
- replace the unicode characters with regular text in testing