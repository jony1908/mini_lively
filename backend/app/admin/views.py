from sqladmin import ModelView
from ..models.user import User
from ..models.admin_user import AdminUser
from ..models.user_profile import UserProfile


class UserAdmin(ModelView, model=User):
    column_list = [
        "id",
        "email", 
        "first_name",
        "last_name",
        "oauth_provider",
        "is_active",
        "is_verified",
        "created_at",
        "updated_at",
    ]
    
    column_details_list = [
        "id",
        "email",
        "first_name", 
        "last_name",
        "oauth_provider",
        "oauth_id",
        "is_active",
        "is_verified", 
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["email", "first_name", "last_name"]
    column_filters = [
        "oauth_provider",
        "is_active", 
        "is_verified",
        "created_at",
    ]
    
    column_sortable_list = [
        "id",
        "email",
        "first_name",
        "last_name", 
        "created_at",
        "updated_at",
    ]
    
    # Don't show password hash in forms
    form_excluded_columns = ["password_hash"]
    
    # Show user-friendly names
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    
    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]


class AdminUserAdmin(ModelView, model=AdminUser):
    column_list = [
        "id",
        "username",
        "is_superuser", 
        "is_active",
        "created_at",
        "updated_at",
    ]
    
    column_details_list = [
        "id",
        "username",
        "is_superuser",
        "is_active",
        "created_at", 
        "updated_at",
    ]
    
    column_searchable_list = ["username"]
    column_filters = [
        "is_superuser",
        "is_active",
        "created_at",
    ]
    
    column_sortable_list = [
        "id", 
        "username",
        "created_at",
        "updated_at",
    ]
    
    # Don't show password hash in forms
    form_excluded_columns = ["password_hash"]
    
    # Show user-friendly names
    name = "Admin User"
    name_plural = "Admin Users"
    icon = "fa-solid fa-user-shield"
    
    # Pagination  
    page_size = 25
    page_size_options = [10, 25, 50, 100]


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [
        "id",
        "user_id",
        "phone_number",
        "city",
        "state", 
        "country",
        "timezone",
        "created_at",
        "updated_at",
    ]
    
    column_details_list = [
        "id",
        "user_id",
        "phone_number",
        "profile_picture_url",
        "city",
        "state",
        "country", 
        "timezone",
        "preferred_activity_types",
        "preferred_schedule",
        "notification_preferences",
        "created_at",
        "updated_at",
    ]
    
    column_searchable_list = ["phone_number", "city", "state", "country"]
    column_filters = [
        "country",
        "state",
        "timezone",
        "created_at",
    ]
    
    column_sortable_list = [
        "id",
        "user_id", 
        "city",
        "state",
        "country",
        "created_at",
        "updated_at",
    ]
    
    # Show user-friendly names
    name = "User Profile"
    name_plural = "User Profiles"
    icon = "fa-solid fa-id-card"
    
    # Pagination
    page_size = 50
    page_size_options = [25, 50, 100, 200]