#!/usr/bin/env python3
"""
Test script for email verification token process
"""

import sys
import os
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.database.connection import get_db
from backend.app.crud.auth import AuthCRUD
from backend.app.utils.email_service import EmailService
from backend.app.schemas.auth import UserCreate

def test_token_verification():
    """Test the complete token verification flow"""
    
    # Test configuration
    backend_url = "http://localhost:8000"
    test_email = "test_verification@example.com"
    test_password = "TestPassword123!"
    
    print("=== Email Verification Token Test ===")
    print(f"Backend URL: {backend_url}")
    print(f"Test email: {test_email}")
    print()
    
    try:
        # Step 1: Create test user via API
        print("[STEP 1] Creating test user via API...")
        register_data = {
            "email": test_email,
            "password": test_password,
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = requests.post(f"{backend_url}/api/auth/register", json=register_data)
        if response.status_code in [200, 201]:
            print(f"[OK] User created successfully: {response.json()}")
        else:
            print(f"[ERROR] Failed to create user: {response.status_code} - {response.text}")
            return False
            
        # Step 2: Get user from database to check initial status
        print("\n[STEP 2] Checking user status in database...")
        db = next(get_db())
        auth_crud = AuthCRUD(db)
        user = auth_crud.get_user_by_email(test_email)
        
        if not user:
            print("[ERROR] User not found in database")
            return False
            
        print(f"[OK] User found - ID: {user.id}, Verified: {user.is_verified}")
        user_id = user.id
        
        # Step 3: Generate verification token manually
        print("\n[STEP 3] Generating verification token...")
        verification_token = EmailService.create_verification_token(user_id)
        print(f"[OK] Token generated: {verification_token[:50]}...")
        
        # Step 4: Test token verification endpoint
        print("\n[STEP 4] Testing token verification endpoint...")
        verify_response = requests.post(
            f"{backend_url}/api/auth/verify-email",
            params={"token": verification_token}
        )
        
        if verify_response.status_code == 200:
            print(f"[OK] Token verification successful: {verify_response.json()}")
        else:
            print(f"[ERROR] Token verification failed: {verify_response.status_code} - {verify_response.text}")
            return False
            
        # Step 5: Check user status after verification
        print("\n[STEP 5] Checking user status after verification...")
        db.refresh(user)  # Refresh from database
        updated_user = auth_crud.get_user_by_email(test_email)
        
        print(f"[OK] User status - ID: {updated_user.id}, Verified: {updated_user.is_verified}")
        
        if updated_user.is_verified:
            print("[OK] Email verification process completed successfully!")
            result = True
        else:
            print("[ERROR] User is still not verified after token verification")
            result = False
            
        # Step 6: Test invalid token
        print("\n[STEP 6] Testing invalid token...")
        invalid_response = requests.post(
            f"{backend_url}/api/auth/verify-email",
            params={"token": "invalid_token_123"}
        )
        
        if invalid_response.status_code == 400:
            print("[OK] Invalid token correctly rejected")
        else:
            print(f"[ERROR] Invalid token handling failed: {invalid_response.status_code}")
            
        return result
        
    except requests.ConnectionError:
        print("[ERROR] Failed to connect to backend server. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed with error: {str(e)}")
        return False
    finally:
        # Cleanup: Delete test user
        print("\n[CLEANUP] Deleting test user...")
        try:
            if 'user_id' in locals():
                success = auth_crud.delete_user_by_email(test_email)
                if success:
                    print("[OK] Test user deleted successfully")
                else:
                    print("[ERROR] Failed to delete test user")
            if 'db' in locals():
                db.close()
        except Exception as e:
            print(f"[ERROR] Cleanup failed: {str(e)}")

if __name__ == "__main__":
    success = test_token_verification()
    if success:
        print("\n[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("\n[FAILED] Some tests failed!")
        sys.exit(1)