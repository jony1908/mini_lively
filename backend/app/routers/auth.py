from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from ..database.connection import get_db
from ..crud.auth import AuthCRUD
from ..schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token, TokenRefresh,
    OAuthLoginRequest, AuthResponse, UserUpdate
)
from ..utils.auth import TokenUtils, OAuthUtils
from ..models.user import User
from ..utils.email_service import EmailService
from ..config.settings import settings

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
    
    # Send verification email
    try:
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "User"
        EmailService.send_verification_email(
            user.email, 
            user_name, 
            user.id
        )
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")
        # Continue with registration even if email fails
    
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


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's basic information."""
    auth_crud = AuthCRUD(db)
    
    # Update user fields if provided
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name
    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)


@router.get("/google")
async def google_auth(request: Request):
    """Initiate Google OAuth login."""
    google_client = OAuthUtils.get_google_oauth()
    # Construct callback URL manually to avoid url_for issues
    base_url = str(request.base_url).rstrip('/')
    redirect_uri = f"{base_url}/api/auth/google/callback"
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
        
        # Redirect to frontend with tokens instead of returning JSON
        from fastapi.responses import RedirectResponse
        from urllib.parse import urlencode
        
        query_params = urlencode({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })
        
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?{query_params}"
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )


@router.get("/apple")
async def apple_auth(request: Request):
    """Initiate Apple OAuth login."""
    apple_client = OAuthUtils.get_apple_oauth()
    # Construct callback URL manually to avoid url_for issues
    base_url = str(request.base_url).rstrip('/')
    redirect_uri = f"{base_url}/api/auth/apple/callback"
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
        
        # Redirect to frontend with tokens instead of returning JSON
        from fastapi.responses import RedirectResponse
        from urllib.parse import urlencode
        
        query_params = urlencode({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        })
        
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?{query_params}"
        return RedirectResponse(url=redirect_url, status_code=302)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )


@router.post("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify user's email address using verification token."""
    user_id = EmailService.verify_email_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    auth_crud = AuthCRUD(db)
    user = auth_crud.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    # Mark user as verified
    user = auth_crud.verify_user_email(user)
    
    # Send welcome email
    try:
        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "User"
        EmailService.send_welcome_email(
            user.email, 
            user_name
        )
    except Exception as e:
        print(f"Failed to send welcome email: {str(e)}")
    
    return {"message": "Email verified successfully"}


@router.post("/resend-verification")
async def resend_verification_email(
    current_user: User = Depends(get_current_user)
):
    """Resend verification email to current user."""
    if current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified"
        )
    
    try:
        user_name = f"{current_user.first_name or ''} {current_user.last_name or ''}".strip() or "User"
        success = EmailService.send_verification_email(
            current_user.email,
            user_name,
            current_user.id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email"
            )
        
        return {"message": "Verification email sent successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send verification email: {str(e)}"
        )


@router.post("/delete-user")
async def delete_user_by_email(request: dict, db: Session = Depends(get_db)):
    """Delete user by email - for testing purposes only."""
    email = request.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    auth_crud = AuthCRUD(db)
    
    success = auth_crud.delete_user_by_email(email)
    if success:
        return {"message": f"User {email} deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or could not be deleted"
        )
