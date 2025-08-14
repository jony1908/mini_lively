
# API Endpoints Documentation

## Overview
The Mini Lively API provides comprehensive endpoints for managing family activity tracking. All endpoints use REST conventions and return JSON responses.

### API Documentation
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

**Base URL**: `http://localhost:8000`
**API Prefix**: `/api`

### API Endpoints
- `POST /api/auth/register` - User registration with email verification
- `POST /api/auth/login` - User login with email/password
- `POST /api/auth/refresh` - Refresh JWT access token
- `GET /api/auth/me` - Get current user profile
- `GET /api/auth/google` - Initiate Google OAuth flow
- `GET /api/auth/apple` - Initiate Apple OAuth flow
- `POST /api/auth/verify-email` - Verify email address
- `POST /api/auth/resend-verification` - Resend verification email
