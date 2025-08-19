from sqladmin import ModelView
from sqladmin.filters import BooleanFilter, AllUniqueStringValuesFilter
from ..models.user import User
from ..models.admin_user import AdminUser
from ..models.member import Member
from ..models.user_profile import UserProfile
from ..models.usertomember import UserToMember


class BasicUserAdmin(ModelView, model=User):
    # Basic working configuration
    name = "User"
    name_plural = "Users"
    category = "Relationships"
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


class BasicMemberAdmin(ModelView, model=Member):
    # Minimal working configuration for Member model
    name = "Member"
    name_plural = "Members"
    category = "Relationships"
    icon = "fa-solid fa-users"
    
    # Basic display with computed age
    column_list = ["id", "first_name", "last_name", "age", "date_of_birth", "gender", "is_active"]
    
    # Proper SQLAdmin filters using available filter classes
    column_filters = [
        BooleanFilter(column=Member.is_active, title="Active Status"),
        AllUniqueStringValuesFilter(column=Member.gender, title="Gender")
    ]
    
    # Search functionality
    column_searchable_list = ["first_name", "last_name"]
    
    # Detailed view with complete member information
    column_details_list = [
        "id",
        "first_name",
        "last_name",
        "age",  # Computed age property
        "date_of_birth",
        "gender",
        "interests",
        "skills",
        "avatar_url",
        "is_active",
        "created_at",
        "updated_at"
    ]
    
    # Form configuration - exclude computed age from forms
    form_excluded_columns = ["age"]  # Age is computed, don't show in create/edit forms
    
    # Basic pagination
    page_size = 50


class BasicUserProfileAdmin(ModelView, model=UserProfile):
    # Basic working configuration
    name = "User Profile"
    name_plural = "User Profiles"
    category = "Relationships"
    icon = "fa-solid fa-id-card"
    
    # Basic display with user information
    column_list = ["id", "user.first_name", "user.last_name", "user.email", "address", "city", "state", "postal_code", "phone_number"]
    
    # Search functionality
    column_searchable_list = ["user.first_name", "user.last_name", "user.email", "address", "postal_code", "phone_number", "city", "state", "country"]
    
    # Detailed view
    column_details_list = [
        "id",
        "user.email",
        "user.first_name", 
        "user.last_name",
        "phone_number",
        "profile_picture_url",
        "address",
        "city",
        "state",
        "postal_code",
        "country",
        "timezone",
        "preferred_activity_types",
        "preferred_schedule", 
        "notification_preferences",
        "created_at",
        "updated_at"
    ]
    
    # Basic filters
    column_filters = [
        AllUniqueStringValuesFilter(column=UserProfile.address, title="Address"),
        AllUniqueStringValuesFilter(column=UserProfile.postal_code, title="Postal Code"),
        AllUniqueStringValuesFilter(column=UserProfile.country, title="Country"),
        AllUniqueStringValuesFilter(column=UserProfile.state, title="State"),
        AllUniqueStringValuesFilter(column=UserProfile.timezone, title="Timezone")
    ]
    
    # Column labels for better display
    column_labels = {
        "user.first_name": "First Name",
        "user.last_name": "Last Name", 
        "user.email": "Email",
        "address": "Address",
        "postal_code": "Zip Code",
        "phone_number": "Phone"
    }
    
    # Basic pagination
    page_size = 50


class BasicUserToMemberAdmin(ModelView, model=UserToMember):
    # Basic working configuration for UserToMember relationships
    name = "User-Member Relationship"
    name_plural = "User-Member Relationships"
    category = "Relationships"
    icon = "fa-solid fa-link"
    
    # Basic display showing key relationship information
    column_list = [
        "id", 
        "user.first_name", 
        "user.last_name", 
        "member.first_name", 
        "member.last_name", 
        "relationship_type.name", 
        "is_manager", 
        "is_shareable", 
        "is_primary",
        "is_active"
    ]
    
    # Filters for relationship management
    column_filters = [
        BooleanFilter(column=UserToMember.is_active, title="Active Status"),
        BooleanFilter(column=UserToMember.is_manager, title="Manager Status"),
        BooleanFilter(column=UserToMember.is_shareable, title="Shareable Status"),
        BooleanFilter(column=UserToMember.is_primary, title="Primary Relationship"),
        BooleanFilter(column=UserToMember.is_visible, title="Visible Status"),
        AllUniqueStringValuesFilter(column=UserToMember.relation, title="Relationship Type")
    ]
    
    # Search functionality
    column_searchable_list = [
        "user.first_name", 
        "user.last_name", 
        "user.email",
        "member.first_name", 
        "member.last_name",
        "relationship_type.name"
    ]
    
    # Detailed view with complete relationship information
    column_details_list = [
        "id",
        "user.email",
        "user.first_name",
        "user.last_name", 
        "member.first_name",
        "member.last_name",
        "relationship_type.name",
        "is_manager",
        "is_shareable", 
        "is_primary",
        "is_active",
        "is_visible",
        "relationship_notes",
        "created_by.first_name",
        "created_by.last_name",
        "invitation_id",
        "created_at",
        "updated_at"
    ]
    
    # Column labels for better display
    column_labels = {
        "user.first_name": "User First Name",
        "user.last_name": "User Last Name",
        "user.email": "User Email",
        "member.first_name": "Member First Name", 
        "member.last_name": "Member Last Name",
        "relationship_type.name": "Relationship Type",
        "is_manager": "Manager",
        "is_shareable": "Shareable",
        "is_primary": "Primary",
        "is_active": "Active",
        "is_visible": "Visible",
        "relationship_notes": "Notes",
        "created_by.first_name": "Created By First Name",
        "created_by.last_name": "Created By Last Name",
        "invitation_id": "Invitation ID"
    }
    
    # Basic pagination
    page_size = 50