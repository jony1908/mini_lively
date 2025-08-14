from sqladmin import ModelView
from ..models.user import User
from ..models.admin_user import AdminUser


class BasicUserAdmin(ModelView, model=User):
    # Basic working configuration
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = ["id", "email", "first_name", "last_name", "is_active"]
    form_excluded_columns = ["password_hash"]
    page_size = 50
    

class BasicAdminUserAdmin(ModelView, model=AdminUser):
    # Basic working configuration
    name = "Admin User" 
    name_plural = "Admin Users"
    icon = "fa-solid fa-user-shield"
    column_list = ["id", "username", "is_superuser", "is_active"]
    form_excluded_columns = ["password_hash"]
    page_size = 25