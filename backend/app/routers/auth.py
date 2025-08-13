from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..dependencies import get_db
from ..crud.auth import AuthCRUD
from ..schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token, TokenRefresh,
    OAuthLoginRequest, AuthResponse
)
from ..auth import TokenUtils, OAuthUtils
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    user_id = TokenUtils.get_user_id_from_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth_crud = AuthCRUD(db)
    user = auth_crud.get_user_by_id(int(user_id))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


@router.post("/register", response_model=AuthResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with email and password."""
    auth_crud = AuthCRUD(db)
    
    # Check if user already exists
    if auth_crud.user_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = auth_crud.create_user_with_password(user_data)
    
    # Generate tokens
    access_token = TokenUtils.create_access_token(data={"sub": str(user.id)})
    refresh_token = TokenUtils.create_refresh_token(data={"sub": str(user.id)})
    
    tokens = Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/login", response_model=AuthResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    auth_crud = AuthCRUD(db)
    
    # Authenticate user
    user = auth_crud.authenticate_user(
        user_credentials.email, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated"
        )
    
    # Generate tokens
    access_token = TokenUtils.create_access_token(data={"sub": str(user.id)})
    refresh_token = TokenUtils.create_refresh_token(data={"sub": str(user.id)})
    
    tokens = Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    payload = TokenUtils.verify_token(token_data.refresh_token, "refresh")
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify user still exists and is active
    auth_crud = AuthCRUD(db)
    user = auth_crud.get_user_by_id(int(user_id))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate new tokens
    access_token = TokenUtils.create_access_token(data={"sub": str(user.id)})
    refresh_token = TokenUtils.create_refresh_token(data={"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.get("/google")
async def google_auth(request: Request):
    """Initiate Google OAuth login."""
    google_client = OAuthUtils.get_google_oauth()
    redirect_uri = str(request.url_for('google_callback'))
    return await google_client.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback."""
    google_client = OAuthUtils.get_google_oauth()
    
    try:
        token = await google_client.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        # Parse user info
        parsed_user_data = OAuthUtils.parse_google_user_info(user_info)
        
        auth_crud = AuthCRUD(db)
        
        # Check if user exists with OAuth
        user = auth_crud.get_user_by_oauth("google", parsed_user_data["oauth_id"])
        
        if not user:
            # Check if user exists with email
            user = auth_crud.get_user_by_email(parsed_user_data["email"])
            
            if user:
                # Link OAuth to existing user
                user = auth_crud.link_oauth_to_existing_user(
                    user, "google", parsed_user_data["oauth_id"]
                )
            else:
                # Create new user
                user = auth_crud.create_user_with_oauth(parsed_user_data)
        
        # Generate tokens
        access_token = TokenUtils.create_access_token(data={"sub": str(user.id)})
        refresh_token = TokenUtils.create_refresh_token(data={"sub": str(user.id)})
        
        tokens = Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        return AuthResponse(
            user=UserResponse.from_orm(user),
            tokens=tokens
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )


@router.get("/apple")
async def apple_auth(request: Request):
    """Initiate Apple OAuth login."""
    apple_client = OAuthUtils.get_apple_oauth()
    redirect_uri = str(request.url_for('apple_callback'))
    return await apple_client.authorize_redirect(request, redirect_uri)


@router.get("/apple/callback")
async def apple_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Apple OAuth callback."""
    apple_client = OAuthUtils.get_apple_oauth()
    
    try:
        token = await apple_client.authorize_access_token(request)
        
        # Apple provides user info differently
        id_token = token.get('id_token')
        user_info = token.get('user', {})
        
        if not id_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Apple"
            )
        
        # Parse user info (Apple provides limited info)
        parsed_user_data = OAuthUtils.parse_apple_user_info(user_info, id_token)
        
        auth_crud = AuthCRUD(db)
        
        # Check if user exists with OAuth
        user = auth_crud.get_user_by_oauth("apple", parsed_user_data["oauth_id"])
        
        if not user:
            # Check if user exists with email
            user = auth_crud.get_user_by_email(parsed_user_data["email"])
            
            if user:
                # Link OAuth to existing user
                user = auth_crud.link_oauth_to_existing_user(
                    user, "apple", parsed_user_data["oauth_id"]
                )
            else:
                # Create new user
                user = auth_crud.create_user_with_oauth(parsed_user_data)
        
        # Generate tokens
        access_token = TokenUtils.create_access_token(data={"sub": str(user.id)})
        refresh_token = TokenUtils.create_refresh_token(data={"sub": str(user.id)})
        
        tokens = Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        return AuthResponse(
            user=UserResponse.from_orm(user),
            tokens=tokens
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )