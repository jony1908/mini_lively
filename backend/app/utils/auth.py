from datetime import datetime, timedelta
from typing import Optional, Union
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from ..config.settings import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
ALGORITHM = "HS256"

# OAuth Configuration
config = Config('.env')
oauth = OAuth(config)

# Google OAuth
if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    google = oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

# Apple OAuth
if settings.APPLE_CLIENT_ID and settings.APPLE_CLIENT_SECRET:
    apple = oauth.register(
        name='apple',
        client_id=settings.APPLE_CLIENT_ID,
        client_secret=settings.APPLE_CLIENT_SECRET,
        authorization_endpoint='https://appleid.apple.com/auth/authorize',
        token_endpoint='https://appleid.apple.com/auth/token',
        client_kwargs={
            'scope': 'name email'
        }
    )


class PasswordUtils:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)


class TokenUtils:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Union[dict, None]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except JWTError:
            return None

    @staticmethod
    def get_user_id_from_token(token: str) -> Optional[int]:
        """Extract user ID from a JWT token."""
        payload = TokenUtils.verify_token(token)
        if payload:
            return payload.get("sub")
        return None


class OAuthUtils:
    @staticmethod
    def get_google_oauth():
        """Get Google OAuth client."""
        if 'google' in oauth._clients:
            return google
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth not configured"
        )

    @staticmethod
    def get_apple_oauth():
        """Get Apple OAuth client."""
        if 'apple' in oauth._clients:
            return apple
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Apple OAuth not configured"
        )

    @staticmethod
    def parse_google_user_info(user_info: dict) -> dict:
        """Parse Google user info into standard format."""
        return {
            "email": user_info.get("email"),
            "first_name": user_info.get("given_name", ""),
            "last_name": user_info.get("family_name", ""),
            "oauth_provider": "google",
            "oauth_id": user_info.get("sub"),
            "is_verified": user_info.get("email_verified", False)
        }

    @staticmethod
    def parse_apple_user_info(user_info: dict, id_token: dict = None) -> dict:
        """Parse Apple user info into standard format."""
        # Apple provides limited user info
        email = user_info.get("email") or (id_token.get("email") if id_token else None)
        
        return {
            "email": email,
            "first_name": user_info.get("firstName", ""),
            "last_name": user_info.get("lastName", ""),
            "oauth_provider": "apple",
            "oauth_id": user_info.get("sub") or (id_token.get("sub") if id_token else None),
            "is_verified": True  # Apple emails are always verified
        }