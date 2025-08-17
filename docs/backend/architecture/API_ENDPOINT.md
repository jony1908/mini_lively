
# API Endpoints Documentation

## Overview
The Mini Lively API provides comprehensive endpoints for managing family activity tracking. All endpoints use REST conventions and return JSON responses.

### API Documentation
- Interactive docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

**Base URL**: `http://localhost:8000`
**API Prefix**: `/api`

### API Endpoints

#### Authentication Endpoints
- `POST /api/auth/register` - User registration with email verification
- `POST /api/auth/login` - User login with email/password
- `POST /api/auth/refresh` - Refresh JWT access token
- `GET /api/auth/me` - Get current user profile
- `PUT /api/auth/me` - Update user's first name and last name
- `GET /api/auth/google` - Initiate Google OAuth flow
- `GET /api/auth/apple` - Initiate Apple OAuth flow
- `POST /api/auth/verify-email` - Verify email address
- `POST /api/auth/resend-verification` - Resend verification email
- `POST /api/auth/delete-user` - Delete user account

#### Profile Management Endpoints
- `GET /api/profile/me` - Get current user's profile
- `POST /api/profile` - Create user profile
- `PUT /api/profile` - Update user profile
- `DELETE /api/profile` - Delete user profile

#### Avatar Management Endpoints
- `POST /api/avatar/upload` - Upload and process user avatar image
- `DELETE /api/avatar/remove` - Remove current user's avatar
- `GET /api/avatar/info` - Get current user's avatar information and upload limits

## Detailed Endpoint Documentation

### Avatar Upload API

#### POST /api/avatar/upload
Upload and process user avatar image with automatic optimization.

**Authentication**: Required (JWT Bearer token)

**Request**:
- Content-Type: `multipart/form-data`
- Body: File upload with key `file`

**File Requirements**:
- Maximum size: 2MB (larger files will be rejected)
- Supported formats: JPEG, PNG, WEBP
- Automatic processing: Resized to 256x256 pixels, converted to JPEG

**Response**:
```json
{
  "success": true,
  "avatar_url": "http://localhost:8000/uploads/avatars/avatar_abc123.jpg",
  "filename": "avatar_abc123.jpg",
  "size": 45672,
  "dimensions": "256x256",
  "message": "Avatar uploaded and processed successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid file format or size
- `401 Unauthorized`: Missing or invalid authentication
- `500 Internal Server Error`: File processing failed

#### DELETE /api/avatar/remove
Remove the current user's avatar from storage and profile.

**Authentication**: Required (JWT Bearer token)

**Response**:
```json
{
  "success": true,
  "message": "Avatar removed successfully"
}
```

**Error Responses**:
- `404 Not Found`: No avatar found to remove
- `401 Unauthorized`: Missing or invalid authentication

#### GET /api/avatar/info
Get current user's avatar information and upload constraints.

**Authentication**: Required (JWT Bearer token)

**Response** (with avatar):
```json
{
  "has_avatar": true,
  "avatar_url": "http://localhost:8000/uploads/avatars/avatar_abc123.jpg",
  "upload_limits": {
    "max_size_mb": 2,
    "supported_formats": ["JPEG", "PNG", "WEBP"],
    "output_size": "256x256"
  }
}
```

**Response** (without avatar):
```json
{
  "has_avatar": false,
  "avatar_url": null,
  "upload_limits": {
    "max_size_mb": 2,
    "supported_formats": ["JPEG", "PNG", "WEBP"],
    "output_size": "256x256"
  }
}
```

### Static File Serving

#### Avatar File Access
Uploaded avatar images are served as static files and can be accessed directly via URL.

**URL Pattern**: `http://localhost:8000/uploads/avatars/{filename}`

**Examples**:
- `http://localhost:8000/uploads/avatars/avatar_abc123.jpg`
- `http://localhost:8000/uploads/avatars/avatar_def456.jpg`

**Notes**:
- All avatar files are automatically processed to 256x256 JPEG format
- Files are stored locally in the `uploads/avatars/` directory
- Unique filenames prevent conflicts (UUID-based naming)
- Public access (no authentication required for viewing)

### Image Processing Features

The avatar upload system includes advanced image processing:

1. **Format Standardization**: All uploads converted to JPEG
2. **Size Optimization**: Resized to exactly 256x256 pixels
3. **Quality Compression**: 85% JPEG quality for optimal file size
4. **Aspect Ratio Handling**: Center-crop to square format
5. **EXIF Orientation**: Automatic rotation based on EXIF data
6. **Transparency Handling**: White background for transparent images

### Integration Notes

- Avatar URLs are automatically saved to the user's profile (`profile_picture_url` field)
- Profile API endpoints return the avatar URL for display
- Frontend components can display avatars directly using the provided URL
- File cleanup occurs when avatars are replaced or removed
