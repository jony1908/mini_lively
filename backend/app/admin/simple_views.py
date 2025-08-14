from sqladmin import ModelView
from ..models.user import User
from ..models.admin_user import AdminUser


class SimpleUserAdmin(ModelView, model=User):
    # Minimal configuration without problematic filters
    column_list = ["id", "email", "first_name", "last_name", "is_active", "is_verified"]
    column_searchable_list = ["email", "first_name", "last_name"]
    form_excluded_columns = ["password_hash", "oauth_id"]
    
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    page_size = 50


class SimpleAdminUserAdmin(ModelView, model=AdminUser):
    # Minimal configuration without problematic filters
    column_list = ["id", "username", "is_superuser", "is_active", "created_at"]
    column_searchable_list = ["username"]
    form_excluded_columns = ["password_hash"]
    
    name = "Admin User"
    name_plural = "Admin Users"
    icon = "fa-solid fa-user-shield"
    page_size = 25