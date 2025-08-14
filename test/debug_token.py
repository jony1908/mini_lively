#!/usr/bin/env python3
"""
Debug token verification
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.utils.email_service import EmailService
from backend.app.utils.auth import TokenUtils
from backend.app.config.settings import settings
from jose import jwt
from datetime import datetime, timedelta

def debug_token_verification():
    """Debug token creation and verification"""
    
    print("=== Token Debug ===")
    user_id = 999  # Test user ID
    
    # Step 1: Create token using EmailService
    print("[STEP 1] Creating token with EmailService...")
    token = EmailService.create_verification_token(user_id)
    print(f"Token: {token}")
    
    # Step 2: Try to verify with EmailService
    print("\n[STEP 2] Verifying token with EmailService...")
    verified_user_id = EmailService.verify_email_token(token)
    print(f"Verified user ID: {verified_user_id}")
    
    # Step 3: Manually decode token to see contents
    print("\n[STEP 3] Manually decoding token...")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(f"Token payload: {payload}")
        print(f"Token type: {payload.get('type')}")
        print(f"Token sub: {payload.get('sub')}")
        print(f"Token exp: {payload.get('exp')} ({datetime.fromtimestamp(payload.get('exp'))})")
    except Exception as e:
        print(f"Failed to decode token: {e}")
    
    # Step 4: Try TokenUtils verification directly
    print("\n[STEP 4] Testing TokenUtils verification...")
    token_payload = TokenUtils.verify_token(token, "email_verification")
    print(f"TokenUtils result: {token_payload}")
    
    # Step 5: Check if it's an expiration issue
    print("\n[STEP 5] Creating fresh token and testing immediately...")
    fresh_token = EmailService.create_verification_token(user_id)
    fresh_result = EmailService.verify_email_token(fresh_token)
    print(f"Fresh token verification: {fresh_result}")

if __name__ == "__main__":
    debug_token_verification()