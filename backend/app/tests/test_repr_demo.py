"""
Demo script to showcase the improved __repr__ methods for all models.
This helps with debugging and logging by providing user-friendly representations.
"""

from datetime import datetime, date, timedelta
from app.models.relationship_type import RelationshipType
from app.models.user_invitation import UserInvitation, InvitationStatus
from app.models.usertomember import UserToMember
from app.models.user import User
from app.models.member import Member
from app.models.user_profile import UserProfile
from app.models.admin_user import AdminUser

def demo_repr_methods():
    print("=" * 80)
    print("DEMO: Improved __repr__ Methods for All Models")
    print("=" * 80)
    
    # RelationshipType examples
    print("\n1. RelationshipType Examples:")
    print("-" * 40)
    
    parent_type = RelationshipType(
        id=1, name="parent", display_name="Parent", 
        is_active=True, is_reciprocal=False, generation_offset=-1
    )
    print(f"Active: {repr(parent_type)}")
    
    spouse_type = RelationshipType(
        id=2, name="spouse", display_name="Spouse",
        is_active=True, is_reciprocal=True, generation_offset=0
    )
    print(f"Reciprocal: {repr(spouse_type)}")
    
    deprecated_type = RelationshipType(
        id=3, name="old_relation", display_name="Deprecated Relation",
        is_active=False, is_reciprocal=False, generation_offset=0
    )
    print(f"Inactive: {repr(deprecated_type)}")
    
    # User examples
    print("\n2. User Examples:")
    print("-" * 40)
    
    active_user = User(
        id=1, email="john@example.com", first_name="John", last_name="Doe",
        is_active=True, is_verified=True
    )
    print(f"Active verified: {repr(active_user)}")
    
    oauth_user = User(
        id=2, email="jane@gmail.com", first_name="Jane", last_name="Smith",
        oauth_provider="google", is_active=True, is_verified=False
    )
    print(f"OAuth unverified: {repr(oauth_user)}")
    
    inactive_user = User(
        id=3, email="bob@example.com", first_name="", last_name="",
        is_active=False, is_verified=True
    )
    print(f"Inactive no name: {repr(inactive_user)}")
    
    # Member examples
    print("\n3. Member Examples:")
    print("-" * 40)
    
    child_member = Member(
        id=1, first_name="Alice", last_name="Johnson",
        date_of_birth=date(2015, 5, 15), gender="female",
        interests=["swimming", "art", "reading"], skills=["cycling", "piano"],
        avatar_url="https://example.com/avatar.jpg", is_active=True
    )
    print(f"Active child: {repr(child_member)}")
    
    simple_member = Member(
        id=2, first_name="Bob", last_name="Wilson",
        date_of_birth=date(1980, 12, 3), is_active=True
    )
    print(f"Simple adult: {repr(simple_member)}")
    
    inactive_member = Member(
        id=3, first_name="Carol", last_name="Brown",
        date_of_birth=date(1990, 8, 20), is_active=False
    )
    print(f"Inactive: {repr(inactive_member)}")
    
    # UserProfile examples
    print("\n4. UserProfile Examples:")
    print("-" * 40)
    
    complete_profile = UserProfile(
        id=1, user_id=1, phone_number="+1234567890",
        city="San Francisco", state="CA", postal_code="94102",
        profile_picture_url="https://example.com/pic.jpg", timezone="America/Los_Angeles"
    )
    print(f"Complete: {repr(complete_profile)}")
    
    minimal_profile = UserProfile(
        id=2, user_id=2, city="Portland", state="OR"
    )
    print(f"Minimal: {repr(minimal_profile)}")
    
    empty_profile = UserProfile(id=3, user_id=3)
    print(f"Empty: {repr(empty_profile)}")
    
    # AdminUser examples
    print("\n5. AdminUser Examples:")
    print("-" * 40)
    
    superuser = AdminUser(
        id=1, username="admin", is_superuser=True, is_active=True
    )
    print(f"Superuser: {repr(superuser)}")
    
    regular_admin = AdminUser(
        id=2, username="moderator", is_superuser=False, is_active=True
    )
    print(f"Regular admin: {repr(regular_admin)}")
    
    inactive_admin = AdminUser(
        id=3, username="old_admin", is_superuser=False, is_active=False
    )
    print(f"Inactive: {repr(inactive_admin)}")
    
    # UserInvitation examples
    print("\n6. UserInvitation Examples:")
    print("-" * 40)
    
    pending_invitation = UserInvitation(
        id=1, inviter_user_id=1, invitee_email="friend@example.com",
        intended_relationship="spouse", status=InvitationStatus.PENDING,
        expires_at=datetime.utcnow() + timedelta(days=5)
    )
    print(f"Pending: {repr(pending_invitation)}")
    
    expired_invitation = UserInvitation(
        id=2, inviter_user_id=1, invitee_email="old@example.com",
        status=InvitationStatus.EXPIRED,
        expires_at=datetime.utcnow() - timedelta(days=2)
    )
    print(f"Expired: {repr(expired_invitation)}")
    
    accepted_invitation = UserInvitation(
        id=3, inviter_user_id=1, invitee_email="family@example.com",
        intended_relationship="sibling", status=InvitationStatus.ACCEPTED,
        expires_at=datetime.utcnow() + timedelta(days=3)
    )
    print(f"Accepted: {repr(accepted_invitation)}")
    
    # UserToMember examples
    print("\n7. UserToMember Examples:")
    print("-" * 40)
    
    manager_relationship = UserToMember(
        id=1, user_id=1, member_id=1, relation="parent",
        is_manager=True, is_shareable=True, is_primary=True, is_active=True
    )
    print(f"Manager primary: {repr(manager_relationship)}")
    
    invited_relationship = UserToMember(
        id=2, user_id=2, member_id=1, relation="aunt_uncle",
        is_manager=False, is_shareable=False, is_primary=False,
        invitation_id=1, is_active=True
    )
    print(f"Via invitation: {repr(invited_relationship)}")
    
    inactive_relationship = UserToMember(
        id=3, user_id=1, member_id=2, relation="spouse",
        is_manager=True, is_shareable=False, is_active=False
    )
    print(f"Inactive: {repr(inactive_relationship)}")
    
    print("\n" + "=" * 80)
    print("All models now have user-friendly __repr__ methods for better debugging!")
    print("=" * 80)

if __name__ == "__main__":
    demo_repr_methods()