#!/usr/bin/env python3
"""
Script to clean up all user-installed packages from global Python
This will remove packages that were installed before setting up the virtual environment
"""

import subprocess
import sys
import os

# List of packages to uninstall (based on pip list --user output)
# Excluding 'pip' itself as it's essential
PACKAGES_TO_REMOVE = [
    'aiofiles',
    'aioredis', 
    'aiosmtplib',
    'aiosqlite',
    'alembic',
    'annotated-types',
    'anyio',
    'async-timeout',
    'Authlib',
    'babel',
    'bcrypt',
    'certifi',
    'cffi',
    'charset-normalizer',
    'click',
    'colorama',
    'cryptography',
    'dnspython',
    'ecdsa',
    'email_validator',
    'fastapi',
    'fastapi-admin',
    'greenlet',
    'h11',
    'httpcore',
    'httptools',
    'httpx',
    'idna',
    'iniconfig',
    'iso8601',
    'itsdangerous',
    'Jinja2',
    'Mako',
    'MarkupSafe',
    'packaging',
    'passlib',
    'pendulum',
    'pluggy',
    'psycopg2-binary',
    'pyasn1',
    'pycparser',
    'pydantic',
    'pydantic_core',
    'PyJWT',
    'pypika-tortoise',
    'pytest',
    'python-dateutil',
    'python-dotenv',
    'python-jose',
    'python-multipart',
    'pytz',
    'PyYAML',
    'requests',
    'requests-toolbelt',
    'rsa',
    'six',
    'sniffio',
    'sqladmin',
    'SQLAlchemy',
    'starlette',
    'tortoise-orm',
    'typing_extensions',
    'typing-inspection',
    'tzdata',
    'urllib3',
    'uvicorn',
    'watchfiles',
    'websockets',
    'WTForms',
]

def uninstall_package(package_name):
    """Uninstall a single package from user directory"""
    try:
        print(f"Uninstalling {package_name}...")
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'uninstall', '-y', package_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] Successfully uninstalled {package_name}")
            return True
        else:
            print(f"[WARNING] Failed to uninstall {package_name}: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[ERROR] Error uninstalling {package_name}: {str(e)}")
        return False

def main():
    print("Cleaning up global Python packages...")
    print(f"Found {len(PACKAGES_TO_REMOVE)} packages to remove")
    print("-" * 60)
    
    successful = 0
    failed = 0
    
    for package in PACKAGES_TO_REMOVE:
        if uninstall_package(package):
            successful += 1
        else:
            failed += 1
        print()  # Empty line for readability
    
    print("-" * 60)
    print(f"Cleanup Summary:")
    print(f"[SUCCESS] Successfully removed: {successful} packages")
    print(f"[FAILED] Failed to remove: {failed} packages")
    
    # Final verification
    print("\nFinal verification - checking remaining user packages...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'list', '--user'
        ], capture_output=True, text=True)
        
        lines = result.stdout.strip().split('\n')[2:]  # Skip header lines
        if lines and lines[0].strip():  # If there are packages listed
            print("Remaining user packages:")
            print(result.stdout)
        else:
            print("[SUCCESS] All user packages successfully removed!")
    except Exception as e:
        print(f"Error checking final state: {e}")

if __name__ == "__main__":
    print("WARNING: This will remove all user-installed Python packages!")
    print("Make sure you have a virtual environment set up for your projects.")
    print("The backend virtual environment at 'backend/venv/' will NOT be affected.")
    print()
    
    response = input("Are you sure you want to continue? (yes/no): ").lower().strip()
    if response in ['yes', 'y']:
        main()
    else:
        print("Cleanup cancelled.")