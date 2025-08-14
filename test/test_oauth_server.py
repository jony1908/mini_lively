#!/usr/bin/env python3
"""
Test OAuth with detailed error handling
"""

import sys
import os
import asyncio
from fastapi.testclient import TestClient

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_oauth_endpoint_directly():
    """Test OAuth endpoint directly with FastAPI test client"""
    
    print("=== Direct OAuth Endpoint Test ===")
    
    try:
        from backend.app.main import app
        client = TestClient(app)
        
        print("[STEP 1] Testing Google OAuth endpoint directly...")
        
        # Make request to OAuth endpoint
        response = client.get("/api/auth/google")
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 500:
            print("\n[ERROR] 500 Internal Server Error occurred")
            
            # Try to get more detailed error info
            if "Internal Server Error" in response.text:
                print("Generic FastAPI 500 error - checking server implementation...")
                
                # Test the OAuth utils directly
                print("\n[STEP 2] Testing OAuth utilities directly...")
                from backend.app.utils.auth import OAuthUtils
                
                try:
                    google_client = OAuthUtils.get_google_oauth()
                    print(f"[OK] OAuth client retrieved: {type(google_client)}")
                    
                    # Test if we can access the authorize_redirect method
                    if hasattr(google_client, 'authorize_redirect'):
                        print("[OK] authorize_redirect method exists")
                    else:
                        print("[ERROR] authorize_redirect method missing")
                        
                except Exception as e:
                    print(f"[ERROR] OAuth utils error: {e}")
                    import traceback
                    traceback.print_exc()
                    
        elif response.status_code == 307:
            print("[OK] OAuth redirect working - this is expected")
            location = response.headers.get('location', '')
            if 'google' in location.lower():
                print(f"[OK] Redirecting to Google: {location[:100]}...")
            
        return response.status_code != 500
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_oauth_route_manually():
    """Test the OAuth route implementation manually"""
    
    print("\n=== Manual OAuth Route Test ===")
    
    try:
        from backend.app.routers.auth import google_auth
        from backend.app.utils.auth import OAuthUtils
        from fastapi import Request
        from starlette.requests import Request as StarletteRequest
        from starlette.datastructures import URL, Headers
        
        print("[STEP 1] Testing google_auth function directly...")
        
        # Create a mock request object
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/auth/google",
            "query_string": b"",
            "headers": [(b"host", b"localhost:8000")],
        }
        
        mock_request = StarletteRequest(scope)
        
        # Test the actual function
        try:
            result = asyncio.run(google_auth(mock_request))
            print(f"[OK] google_auth function executed successfully")
            print(f"Result type: {type(result)}")
            return True
        except Exception as e:
            print(f"[ERROR] google_auth function failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"[ERROR] Manual test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if all OAuth dependencies are installed"""
    
    print("\n=== Dependency Check ===")
    
    required_modules = [
        'authlib',
        'starlette', 
        'fastapi',
        'jose'
    ]
    
    all_good = True
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"[OK] {module} - installed")
        except ImportError as e:
            print(f"[ERROR] {module} - missing: {e}")
            all_good = False
            
    return all_good

if __name__ == "__main__":
    print("Testing OAuth endpoint with detailed error handling...\n")
    
    deps_ok = check_dependencies()
    direct_test_ok = test_oauth_endpoint_directly()
    manual_test_ok = test_oauth_route_manually()
    
    if deps_ok and direct_test_ok and manual_test_ok:
        print("\n[SUCCESS] OAuth endpoint tests completed successfully!")
    else:
        print("\n[FAILED] OAuth endpoint has issues!")
        
    print(f"\nDependencies OK: {deps_ok}")
    print(f"Direct test OK: {direct_test_ok}")
    print(f"Manual test OK: {manual_test_ok}")