#!/usr/bin/env python3
"""
Test script to show the email verification content that would be sent
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.utils.email_service import EmailService

def test_email_content():
    """Test and display the email verification content"""
    
    # Test user data
    test_email = "hfyz4@163.com"
    test_name = "Test User"
    test_user_id = 999
    
    print("=" * 50)
    print("EMAIL VERIFICATION TEST SUMMARY")
    print("=" * 50)
    print(f"Recipient: {test_email}")
    print(f"User name: {test_name}")
    print(f"User ID: {test_user_id}")
    print()
    
    # Create verification token to show what would be generated
    try:
        verification_token = EmailService.create_verification_token(test_user_id)
        print("VERIFICATION DETAILS:")
        print(f"Token generated: {verification_token[:50]}...")
        print(f"Frontend URL: http://localhost:5174")
        print(f"Full verification URL: http://localhost:5174/verify-email?token={verification_token[:30]}...")
        print()
        
        # Send the actual email
        success = EmailService.send_verification_email(
            user_email=test_email,
            user_name=test_name,
            user_id=test_user_id
        )
        
        print("EMAIL SENDING RESULT:")
        if success:
            print("[SUCCESS] Verification email sent successfully!")
            print(f"Email delivered to: {test_email}")
            print()
            print("EMAIL FEATURES:")
            print("- Professional HTML design with Mini Lively branding")
            print("- Click-to-verify button")
            print("- Fallback verification URL for copy/paste")
            print("- 24-hour expiration notice") 
            print("- Plain text version for accessibility")
        else:
            print("[ERROR] Failed to send verification email")
            
    except Exception as e:
        print(f"[ERROR] Error in email verification: {str(e)}")

if __name__ == "__main__":
    test_email_content()