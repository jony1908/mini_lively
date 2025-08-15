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

### User Management Category
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

### Content Category
- **Children**: Complete family member management with advanced features
  - **Computed Age Display**: Automatic age calculation from date of birth (e.g., "Emma Doe, Age: 10")
  - **Advanced Search**: Child names (first/last) and parent email search
  - **Smart Filtering**: 
    - BooleanFilter for active status (dropdown: Active/Inactive)
    - AllUniqueStringValuesFilter for gender (dropdown with database values)
  - **Parent Relationship Integration**:
    - Display parent email in list view for quick identification
    - Full parent information in detail view (email, first name, last name)
    - Search children by parent email address
  - **Enhanced Profile Management**:
    - Complete child profiles with interests and skills
    - Date of birth with automatic age computation
    - Gender and activity status tracking
  - **Professional Admin Interface**:
    - Organized under Content category for logical grouping
    - Form validation with computed fields properly excluded
    - 50-item pagination with configurable options
    - FontAwesome child icon for visual identification
  - **Database Integration**: 
    - Proper SQLAlchemy relationships with User model
    - Foreign key constraints ensuring data integrity
    - Automatic timestamps for creation and updates

## Adding New Models
To add admin views for new models:

1. Create your SQLAlchemy model in `app/models/`
2. Add a corresponding admin view in `app/admin/basic_views.py`:
```python
class YourModelAdmin(ModelView, model=YourModel):
    name = "Your Model"
    name_plural = "Your Models"
    category = "Content"  # Or "User Management" or create new category
    icon = "fa-solid fa-icon-name"
    column_list = [YourModel.field1, YourModel.field2]
    # Configure other properties as needed
```
3. Register the view in `app/main.py`:
```python
from .admin.basic_views import YourModelAdmin
admin.add_view(YourModelAdmin)
```

### Admin Interface Organization
The admin interface is organized into categories for better navigation:
- **User Management**: User accounts and admin management
- **Content**: Family data, children profiles, and activity content
- You can create additional categories by setting the `category` parameter in ModelView classes

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