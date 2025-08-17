"""
Test script for avatar upload functionality.
Tests the image processing and API endpoints.
"""

import requests
import io
from PIL import Image
import json
import sys
import os

# Add the backend path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.utils.image_processing import ImageProcessor

def create_test_image(width=500, height=400, color=(255, 100, 100)):
    """Create a test image for upload testing."""
    image = Image.new('RGB', (width, height), color)
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def test_image_processing():
    """Test the image processing functionality."""
    print("Testing Image Processing...")
    
    # Create test images
    test_cases = [
        {"size": (500, 400), "color": (255, 100, 100), "name": "landscape"},
        {"size": (400, 500), "color": (100, 255, 100), "name": "portrait"},
        {"size": (300, 300), "color": (100, 100, 255), "name": "square"},
        {"size": (1000, 800), "color": (255, 255, 100), "name": "large"},
    ]
    
    for case in test_cases:
        print(f"\nTesting {case['name']} image ({case['size'][0]}x{case['size'][1]})...")
        
        # Create test image
        img_data = create_test_image(case['size'][0], case['size'][1], case['color'])
        
        try:
            # Process image
            processed_data, filename = ImageProcessor.process_avatar(img_data, f"test_{case['name']}.jpg")
            
            # Verify processing
            processed_img = Image.open(io.BytesIO(processed_data))
            
            print(f"  [OK] Original size: {case['size']}")
            print(f"  [OK] Processed size: {processed_img.size}")
            print(f"  [OK] Expected size: {ImageProcessor.AVATAR_SIZE}")
            print(f"  [OK] Filename: {filename}")
            print(f"  [OK] File size: {len(processed_data)} bytes")
            
            # Verify it's the correct size
            if processed_img.size == ImageProcessor.AVATAR_SIZE:
                print(f"  [OK] Size correct!")
            else:
                print(f"  [ERROR] Size incorrect! Expected {ImageProcessor.AVATAR_SIZE}, got {processed_img.size}")
            
            # Test thumbnail creation
            thumbnail_data = ImageProcessor.create_thumbnail(processed_data)
            thumbnail_img = Image.open(io.BytesIO(thumbnail_data))
            print(f"  [OK] Thumbnail size: {thumbnail_img.size}")
            
        except Exception as e:
            print(f"  [ERROR] Error processing {case['name']}: {str(e)}")

def test_file_validation():
    """Test file validation functionality."""
    print("\nTesting File Validation...")
    
    # Test valid image
    valid_img = create_test_image(200, 200)
    is_valid = ImageProcessor.validate_image_format(valid_img)
    print(f"Valid JPEG: {'[OK]' if is_valid else '[ERROR]'}")
    
    # Test invalid data
    invalid_data = b"This is not an image"
    is_valid = ImageProcessor.validate_image_format(invalid_data)
    print(f"Invalid data: {'[OK]' if not is_valid else '[ERROR]'}")

def test_api_endpoints():
    """Test the avatar API endpoints (requires running server)."""
    print("\nTesting API Endpoints...")
    
    base_url = "http://localhost:8001"
    
    # Test health endpoint first
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("[OK] Server is running")
        else:
            print("[ERROR] Server health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Make sure it's running on localhost:8000")
        return
    
    # Test avatar info endpoint (should require auth)
    try:
        response = requests.get(f"{base_url}/api/avatar/info")
        if response.status_code == 401 or response.status_code == 403:
            print("[OK] Avatar info endpoint properly requires authentication")
        elif response.status_code == 422 and "Not authenticated" in str(response.json()):
            print("[OK] Avatar info endpoint properly requires authentication") 
        else:
            print(f"[INFO] Avatar info endpoint returned: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Error testing avatar info: {str(e)}")

if __name__ == "__main__":
    print("=== Avatar Upload Functionality Test ===\n")
    
    # Test image processing
    test_image_processing()
    
    # Test file validation
    test_file_validation()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n=== Test Complete ===")
    print("\nTo test the full upload functionality:")
    print("1. Start the backend server: python -m uvicorn app.main:app --reload")
    print("2. Start the frontend server: npm run dev")
    print("3. Register/login to the application")
    print("4. Go to Profile Form and test avatar upload")