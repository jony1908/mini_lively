from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from ..models.user import User
from ..schemas.auth import UserCreate
from ..auth import PasswordUtils


class AuthCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_oauth(self, provider: str, oauth_id: str) -> Optional[User]:
        """Get user by OAuth provider and ID."""
        return self.db.query(User).filter(
            User.oauth_provider == provider,
            User.oauth_id == oauth_id
        ).first()

    def create_user_with_password(self, user_data: UserCreate) -> User:
        """Create a new user with email/password authentication."""
        hashed_password = PasswordUtils.get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            oauth_provider=None,
            oauth_id=None,
            is_verified=False
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def create_user_with_oauth(self, user_data: dict) -> User:
        """Create a new user with OAuth authentication."""
        db_user = User(
            email=user_data["email"],
            password_hash=None,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            oauth_provider=user_data["oauth_provider"],
            oauth_id=user_data["oauth_id"],
            is_verified=user_data.get("is_verified", False)
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(email)
        if not user or not user.password_hash:
            return None
        
        if not PasswordUtils.verify_password(password, user.password_hash):
            return None
        
        return user

    def update_user_password(self, user: User, new_password: str) -> User:
        """Update user password."""
        user.password_hash = PasswordUtils.get_password_hash(new_password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_user_email(self, user: User) -> User:
        """Mark user email as verified."""
        user.is_verified = True
        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate_user(self, user: User) -> User:
        """Deactivate user account."""
        user.is_active = False
        self.db.commit()
        self.db.refresh(user)
        return user

    def activate_user(self, user: User) -> User:
        """Activate user account."""
        user.is_active = True
        self.db.commit()
        self.db.refresh(user)
        return user

    def user_exists(self, email: str) -> bool:
        """Check if user exists by email."""
        return self.db.query(User).filter(User.email == email).first() is not None

    def link_oauth_to_existing_user(self, user: User, provider: str, oauth_id: str) -> User:
        """Link OAuth account to existing user."""
        user.oauth_provider = provider
        user.oauth_id = oauth_id
        if not user.is_verified:
            user.is_verified = True
        self.db.commit()
        self.db.refresh(user)
        return user