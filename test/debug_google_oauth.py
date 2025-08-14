#!/usr/bin/env python3
"""
Debug Google OAuth issues
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def debug_oauth_config():
    """Debug OAuth configuration"""
    
    print("=== Google OAuth Debug ===")
    
    try:
        from backend.app.config.settings import settings
        from backend.app.utils.auth import oauth, OAuthUtils
        
        print(f"Settings loaded successfully")
        print(f"GOOGLE_CLIENT_ID: {settings.GOOGLE_CLIENT_ID[:20]}..." if settings.GOOGLE_CLIENT_ID else "Not set")
        print(f"GOOGLE_CLIENT_SECRET: {settings.GOOGLE_CLIENT_SECRET[:20]}..." if settings.GOOGLE_CLIENT_SECRET else "Not set")
        
        print(f"\nOAuth object: {oauth}")
        print(f"OAuth clients: {oauth._clients.keys() if hasattr(oauth, '_clients') else 'No _clients attribute'}")
        
        # Try to get Google client
        print("\nTrying to get Google OAuth client...")
        try:
            google_client = OAuthUtils.get_google_oauth()
            print(f"Google client: {google_client}")
            print(f"Client ID: {getattr(google_client, 'client_id', 'No client_id attr')}")
        except Exception as e:
            print(f"Error getting Google client: {e}")
            
        # Check if google is registered
        print(f"\nChecking if 'google' is in oauth clients...")
        if hasattr(oauth, '_clients'):
            if 'google' in oauth._clients:
                print("✓ Google client is registered")
            else:
                print("✗ Google client is NOT registered")
                print(f"Available clients: {list(oauth._clients.keys())}")
        
        # Test manual client creation
        print(f"\nTesting manual Google OAuth registration...")
        from authlib.integrations.starlette_client import OAuth
        from starlette.config import Config
        
        config = Config('.env')
        test_oauth = OAuth(config)
        
        if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
            google = test_oauth.register(
                name='google',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
                client_kwargs={
                    'scope': 'openid email profile'
                }
            )
            print(f"✓ Manual Google client registration successful: {google}")
        else:
            print("✗ Missing credentials for manual registration")
            
    except Exception as e:
        print(f"Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_oauth_config()