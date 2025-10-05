#!/usr/bin/env python3
"""
Test script to check if all dependencies are working correctly
"""

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import sqlite3
        print("✅ sqlite3 - OK")
    except ImportError as e:
        print(f"❌ sqlite3 - FAILED: {e}")
        
    try:
        from cryptography.fernet import Fernet
        print("✅ cryptography - OK")
    except ImportError as e:
        print(f"❌ cryptography - FAILED: {e}")
        
    try:
        import psutil
        print("✅ psutil - OK")
    except ImportError as e:
        print(f"❌ psutil - FAILED: {e}")
        
    try:
        import yaml
        print("✅ pyyaml - OK")
    except ImportError as e:
        print(f"❌ pyyaml - FAILED: {e}")
        
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
        print("✅ PyQt6 - OK")
    except ImportError as e:
        print(f"❌ PyQt6 - FAILED: {e}")
        print("   Install with: pip install PyQt6")

def test_core_modules():
    """Test if our core modules can be imported"""
    print("\nTesting core modules...")
    
    try:
        from core.account_manager import AccountManager
        print("✅ AccountManager - OK")
        
        # Test basic functionality
        am = AccountManager(db_path="test_accounts.db")
        print("✅ AccountManager initialization - OK")
        
        # Clean up test file
        import os
        if os.path.exists("test_accounts.db"):
            os.remove("test_accounts.db")
        if os.path.exists("key.key"):
            os.remove("key.key")
            
    except Exception as e:
        print(f"❌ AccountManager - FAILED: {e}")
        
    try:
        from core.riot_client import RiotClient
        print("✅ RiotClient - OK")
        
        # Test basic functionality
        rc = RiotClient()
        is_running = rc.is_running()
        print(f"✅ RiotClient.is_running() - OK (result: {is_running})")
        
    except Exception as e:
        print(f"❌ RiotClient - FAILED: {e}")

def test_gui_modules():
    """Test if GUI modules can be imported"""
    print("\nTesting GUI modules...")
    
    try:
        from gui.main_window import MainWindow
        print("✅ MainWindow - OK")
    except Exception as e:
        print(f"❌ MainWindow - FAILED: {e}")
        
    try:
        from gui.account_dialog import AccountDialog
        print("✅ AccountDialog - OK")
    except Exception as e:
        print(f"❌ AccountDialog - FAILED: {e}")

def main():
    print("Riot Account Switcher - Dependency Test")
    print("=" * 40)
    
    test_imports()
    test_core_modules()
    test_gui_modules()
    
    print("\n" + "=" * 40)
    print("Test completed!")
    print("\nIf you see any FAILED tests, install the missing dependencies:")
    print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()