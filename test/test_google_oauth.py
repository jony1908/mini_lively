#!/usr/bin/env python3
"""
Test script for Google OAuth login
"""

import sys
import os
import requests
from urllib.parse import urlparse, parse_qs

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.app.config.settings import settings

def test_google_oauth():
    """Test Google OAuth configuration and endpoints"""
    
    backend_url = "http://localhost:8000"
    
    print("=== Google OAuth Test ===")
    print(f"Backend URL: {backend_url}")
    print()
    
    # Step 1: Check configuration
    print("[STEP 1] Checking Google OAuth configuration...")
    print(f"Google Client ID configured: {bool(settings.GOOGLE_CLIENT_ID)}")
    print(f"Google Client Secret configured: {bool(settings.GOOGLE_CLIENT_SECRET)}")
    
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        print("[ERROR] Google OAuth not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env")
        print("\nTo configure Google OAuth:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google+ API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Add authorized redirect URI: http://localhost:8000/api/auth/google/callback")
        print("6. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env file")
        return False
    
    print("[OK] Google OAuth credentials are configured")
    
    try:
        # Step 2: Test OAuth initiation endpoint
        print("\n[STEP 2] Testing Google OAuth initiation...")
        response = requests.get(f"{backend_url}/api/auth/google", allow_redirects=False)
        
        if response.status_code == 307:  # Redirect to Google
            redirect_url = response.headers.get('location', '')
            print(f"[OK] OAuth initiation successful - redirects to Google")
            print(f"Redirect URL: {redirect_url[:100]}...")
            
            # Parse the redirect URL to verify it's Google
            parsed_url = urlparse(redirect_url)
            if 'accounts.google.com' in parsed_url.netloc:
                print("[OK] Correctly redirects to Google OAuth")
            else:
                print(f"[ERROR] Unexpected redirect destination: {parsed_url.netloc}")
                return False
                
        elif response.status_code == 500:
            print("[ERROR] Internal server error - likely configuration issue")
            print(f"Response: {response.text}")
            return False
        else:
            print(f"[ERROR] Unexpected response: {response.status_code} - {response.text}")
            return False
            
        # Step 3: Test callback endpoint (simulate)
        print("\n[STEP 3] Testing callback endpoint structure...")
        callback_response = requests.get(f"{backend_url}/api/auth/google/callback")
        
        # This will fail because we don't have a real OAuth code, but should give a specific error
        if callback_response.status_code == 400:
            print("[OK] Callback endpoint exists and handles missing OAuth data correctly")
        else:
            print(f"[INFO] Callback response: {callback_response.status_code} - {callback_response.text[:200]}...")
            
        # Step 4: Manual OAuth flow test (requires user interaction)
        print("\n[STEP 4] Manual OAuth Test")
        print("To test the complete OAuth flow:")
        print(f"1. Open browser and visit: {backend_url}/api/auth/google")
        print("2. Complete Google OAuth flow")
        print("3. You should be redirected back with authentication tokens")
        print("4. Check browser developer tools for the final response")
        
        return True
        
    except requests.ConnectionError:
        print("[ERROR] Failed to connect to backend server. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed with error: {str(e)}")
        return False

def test_oauth_utils():
    """Test OAuth utility functions"""
    print("\n=== OAuth Utils Test ===")
    
    try:
        from backend.app.utils.auth import OAuthUtils
        
        # Test Google client access
        print("[STEP 1] Testing Google OAuth client access...")
        try:
            google_client = OAuthUtils.get_google_oauth()
            print("[OK] Google OAuth client accessible")
        except Exception as e:
            print(f"[ERROR] Google OAuth client not accessible: {str(e)}")
            return False
            
        # Test user info parsing
        print("\n[STEP 2] Testing Google user info parsing...")
        sample_google_user_info = {
            "sub": "123456789",
            "email": "test@gmail.com",
            "given_name": "Test",
            "family_name": "User",
            "email_verified": True
        }
        
        parsed_data = OAuthUtils.parse_google_user_info(sample_google_user_info)
        expected_fields = ["email", "first_name", "last_name", "oauth_provider", "oauth_id", "is_verified"]
        
        all_fields_present = all(field in parsed_data for field in expected_fields)
        if all_fields_present:
            print("[OK] Google user info parsing works correctly")
            print(f"Sample parsed data: {parsed_data}")
        else:
            print(f"[ERROR] Missing fields in parsed data: {parsed_data}")
            return False
            
        return True
        
    except Exception as e:
        print(f"[ERROR] OAuth utils test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Google OAuth functionality...\n")
    
    oauth_test_success = test_google_oauth()
    utils_test_success = test_oauth_utils()
    
    if oauth_test_success and utils_test_success:
        print("\n[SUCCESS] Google OAuth tests completed successfully!")
        print("\nNote: For complete testing, you need to:")
        print("1. Configure Google OAuth credentials in .env")
        print("2. Manually test the OAuth flow in a browser")
        sys.exit(0)
    else:
        print("\n[FAILED] Some Google OAuth tests failed!")
        sys.exit(1)