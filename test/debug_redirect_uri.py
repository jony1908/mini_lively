#!/usr/bin/env python3
"""
Debug redirect URI for Google OAuth
"""

import sys
import os
import requests

def debug_redirect_uri():
    """Debug what redirect URI is being sent"""
    
    backend_url = "http://localhost:8000"
    
    print("=== Google OAuth Redirect URI Debug ===")
    print(f"Backend URL: {backend_url}")
    print()
    
    try:
        print("[STEP 1] Making request to Google OAuth endpoint...")
        
        # Make request and capture the redirect
        response = requests.get(f"{backend_url}/api/auth/google", allow_redirects=False)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 307:
            redirect_url = response.headers.get('location', '')
            print(f"\n[STEP 2] Analyzing redirect URL...")
            print(f"Full redirect URL: {redirect_url}")
            
            # Parse the redirect URL to extract redirect_uri parameter
            from urllib.parse import urlparse, parse_qs
            
            parsed = urlparse(redirect_url)
            query_params = parse_qs(parsed.query)
            
            print(f"\n[STEP 3] OAuth parameters:")
            for key, value in query_params.items():
                print(f"  {key}: {value[0] if value else 'None'}")
                
            redirect_uri = query_params.get('redirect_uri', ['Not found'])[0]
            print(f"\n[STEP 4] Redirect URI being sent to Google:")
            print(f"  {redirect_uri}")
            
            print(f"\n[STEP 5] Instructions to fix Google Cloud Console:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Select your project")
            print("3. Go to APIs & Services > Credentials")
            print("4. Edit your OAuth 2.0 Client ID")
            print("5. Under 'Authorized redirect URIs', add:")
            print(f"   {redirect_uri}")
            print("6. Save the changes")
            
        else:
            print(f"[ERROR] Unexpected response: {response.text}")
            
    except requests.ConnectionError:
        print("[ERROR] Could not connect to backend server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"[ERROR] Debug failed: {e}")

if __name__ == "__main__":
    debug_redirect_uri()