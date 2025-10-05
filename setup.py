#!/usr/bin/env python3
"""
Installation and setup script for Riot Account Switcher
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required Python packages"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ["backups", "account_backups"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_python_version():
    """Check if Python version is compatible"""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {major}.{minor}")
        return False
    print(f"✅ Python version OK: {major}.{minor}")
    return True

def main():
    print("Riot Account Switcher - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        print("\nPlease upgrade to Python 3.8 or higher.")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please check the error messages above.")
        return
    
    # Create directories
    create_directories()
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("\nYou can now run the application with:")
    print("python main.py")
    print("\nOr test the installation with:")
    print("python test_setup.py")

if __name__ == "__main__":
    main()