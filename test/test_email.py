#!/usr/bin/env python3
"""
Test script to send verification email directly using the EmailService
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.utils.email_service import EmailService

def test_verification_email():
    """Test sending a verification email"""
    
    # Test user data
    test_email = "hfyz4@163.com"
    test_name = "Test User"
    test_user_id = 999  # Mock user ID
    
    print(f"Testing email verification for: {test_email}")
    print(f"User name: {test_name}")
    print(f"User ID: {test_user_id}")
    
    try:
        # Send verification email
        success = EmailService.send_verification_email(
            user_email=test_email,
            user_name=test_name,
            user_id=test_user_id
        )
        
        if success:
            print("[SUCCESS] Verification email sent successfully!")
            print(f"Email sent to: {test_email}")
        else:
            print("[ERROR] Failed to send verification email")
            
    except Exception as e:
        print(f"[ERROR] Error sending verification email: {str(e)}")

if __name__ == "__main__":
    test_verification_email()