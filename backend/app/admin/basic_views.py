from sqladmin import ModelView
from sqladmin.filters import BooleanFilter, AllUniqueStringValuesFilter
from ..models.user import User
from ..models.admin_user import AdminUser
from ..models.child import Child


class BasicUserAdmin(ModelView, model=User):
    # Basic working configuration
    name = "User"
    name_plural = "Users"
    category = "User Management"
    icon = "fa-solid fa-user"
    column_list = ["id", "email", "first_name", "last_name", "is_active"]
    form_excluded_columns = ["password_hash"]
    page_size = 50
    

class BasicAdminUserAdmin(ModelView, model=AdminUser):
    # Basic working configuration
    name = "Admin User" 
    name_plural = "Admin Users"
    category = "User Management"
    icon = "fa-solid fa-user-shield"
    column_list = ["id", "username", "is_superuser", "is_active"]
    form_excluded_columns = ["password_hash"]
    page_size = 25


class BasicChildAdmin(ModelView, model=Child):
    # Minimal working configuration for Child model
    name = "Child"
    name_plural = "Children"
    category = "Content"
    icon = "fa-solid fa-child"
    
    # Basic display with parent information and computed age
    column_list = ["id", "first_name", "last_name", "age", "date_of_birth", "gender", "parent.email", "is_active"]
    
    # Proper SQLAdmin filters using available filter classes
    column_filters = [
        BooleanFilter(column=Child.is_active, title="Active Status"),
        AllUniqueStringValuesFilter(column=Child.gender, title="Gender")
    ]
    
    # Search functionality - simplified to avoid duplicate table joins
    column_searchable_list = ["first_name", "last_name", "parent.email"]
    
    # Detailed view with complete child and parent information
    column_details_list = [
        "id",
        "first_name",
        "last_name",
        "age",  # Computed age property
        "date_of_birth",
        "gender",
        "interests",
        "skills",
        "parent.email",
        "parent.first_name",
        "parent.last_name",
        "is_active",
        "created_at",
        "updated_at"
    ]
    
    # Form configuration - exclude computed age from forms
    form_excluded_columns = ["age"]  # Age is computed, don't show in create/edit forms
    
    # Basic pagination
    page_size = 50