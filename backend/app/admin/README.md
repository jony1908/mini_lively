# Admin Dashboard Setup

## Overview
The FastAPI backend now includes an admin dashboard powered by SQLAdmin, providing a web-based interface for managing database records.

## Access
- **URL**: `http://localhost:8000/admin`

### Database Superuser (Primary)
- **Username**: `hfyz4@163.com`
- **Password**: `1988hfyz`
- **Role**: Superuser with full admin access

### Fallback Admin (Settings-based)
- **Default Username**: `admin` (configurable via `ADMIN_USERNAME` env var)
- **Default Password**: `admin123` (configurable via `ADMIN_PASSWORD` env var)

## Features
- User management (view, edit, delete users)
- Search and filter capabilities
- Pagination for large datasets
- Secure authentication
- Responsive web interface

## Configuration
Admin settings can be configured in the `.env` file:
```bash
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password
```

## Current Models
- **Users**: Complete CRUD operations for user accounts
  - View user details, OAuth information, verification status
  - Search by email, name
  - Filter by provider, active status, verification status
  - Password hashes are hidden for security

- **Admin Users**: Management of admin dashboard users
  - View admin user details, superuser status
  - Search by username
  - Filter by superuser status, active status
  - Password hashes are hidden for security
  - Create additional admin users through the interface

## Adding New Models
To add admin views for new models:

1. Create your SQLAlchemy model in `app/models/`
2. Add a corresponding admin view in `app/admin/views.py`:
```python
class YourModelAdmin(ModelView, model=YourModel):
    column_list = [YourModel.field1, YourModel.field2]
    # Configure other properties as needed
```
3. Register the view in `app/main.py`:
```python
admin.add_view(YourModelAdmin)
```

## Running the Backend

### Using Virtual Environment (Recommended)
The backend now uses a Python virtual environment for dependency isolation:

**Windows (Command Prompt)**:
```cmd
cd backend
run_backend.bat
```

**Windows (Git Bash/PowerShell)**:
```bash
cd backend  
./run_backend.sh
```

**Manual activation**:
```bash
cd backend
venv/Scripts/python.exe -m app.main
```

### Alternative (Global Python)
```bash
cd backend
python -m app.main
```

## Creating Additional Admin Users

To create more admin users, you can:

1. **Use the existing admin interface** (recommended):
   - Login with the superuser account
   - Navigate to "Admin Users" section
   - Click "Create" to add new admin users
   - Set appropriate permissions (superuser vs regular admin)

2. **Use the script**:
   ```bash
   # Modify the create_superuser.py script with new credentials
   python create_superuser.py
   ```

## Authentication Flow
The admin authentication system tries multiple methods:
1. **Database Authentication**: Checks `admin_users` table for valid credentials
2. **Settings Fallback**: Falls back to environment variable credentials
3. **Session Management**: Maintains secure login sessions with user info

## Security Notes
- Database superuser credentials are securely hashed with bcrypt
- Admin authentication is session-based with secure tokens
- All admin operations are logged
- Superuser status controls access to sensitive operations
- Consider implementing role-based access for multiple admin users