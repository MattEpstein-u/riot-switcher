#!/usr/bin/env python3
"""
Test account switching functionality
"""

from core.account_manager import AccountManager
from core.riot_client import RiotClient
import time

def test_account_management():
    print("=== Account Management Test ===")
    
    # Create account manager
    am = AccountManager(db_path="test_accounts.db")
    
    # Add test accounts (don't use real passwords!)
    print("1. Adding test accounts...")
    
    try:
        account1_id = am.add_account("test_user1@example.com", "test_pass1", "Test Account 1")
        account2_id = am.add_account("test_user2@example.com", "test_pass2", "Test Account 2")
        print(f"   ✅ Added account 1: {account1_id}")
        print(f"   ✅ Added account 2: {account2_id}")
    except Exception as e:
        print(f"   ❌ Error adding accounts: {e}")
        return
        
    # List accounts
    print("\n2. Listing accounts...")
    accounts = am.get_all_accounts()
    for account in accounts:
        print(f"   - {account['display_name']} ({account['username']})")
        
    # Test getting account with password
    print("\n3. Testing account retrieval...")
    full_account = am.get_account(account1_id)
    if full_account:
        print(f"   ✅ Retrieved account: {full_account['display_name']}")
        print(f"   Username: {full_account['username']}")
        print(f"   Password decrypted: {'✅ Yes' if full_account['password'] == 'test_pass1' else '❌ No'}")
    else:
        print("   ❌ Could not retrieve account")
        
    # Cleanup
    print("\n4. Cleaning up test data...")
    try:
        am.delete_account(account1_id)
        am.delete_account(account2_id)
        import os
        if os.path.exists("test_accounts.db"):
            os.remove("test_accounts.db")
        if os.path.exists("key.key"):
            os.remove("key.key")
        print("   ✅ Cleanup complete")
    except Exception as e:
        print(f"   ⚠️ Cleanup warning: {e}")

def test_switching_logic():
    print("=== Account Switching Logic Test ===")
    
    rc = RiotClient()
    
    # Test account data (fake)
    test_account = {
        'display_name': 'Test Account',
        'username': 'test@example.com',
        'password': 'fake_password'
    }
    
    print("1. Current status before switch:")
    print(f"   Client running: {rc.is_running()}")
    print(f"   User logged in: {rc.is_logged_in()}")
    print(f"   Current user: {rc.get_current_user()}")
    
    if rc.is_running() and rc.is_logged_in():
        print("\n2. Testing logout without actual switching...")
        
        # Ask user if they want to test logout
        response = input("   Do you want to test logout? (y/N): ").lower().strip()
        if response == 'y':
            print("   Testing force logout...")
            success = rc.force_logout()
            print(f"   Logout result: {'✅ Success' if success else '❌ Failed'}")
            
            time.sleep(2)
            print("\n3. Status after logout:")
            print(f"   Client running: {rc.is_running()}")
            print(f"   User logged in: {rc.is_logged_in()}")
            print(f"   Current user: {rc.get_current_user()}")
        else:
            print("   Skipping logout test")
    else:
        print("\n2. No active session to test logout with")
        
        # Test session clearing anyway
        print("   Testing session clearing...")
        success = rc.clear_current_session()
        print(f"   Session clear result: {'✅ Success' if success else '❌ Failed'}")

def main():
    print("Riot Account Switcher - Functionality Test")
    print("=" * 50)
    
    print("\nChoose test:")
    print("1. Account Management (encryption, storage)")
    print("2. Switching Logic (logout, session clearing)")
    print("3. Both tests")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        test_account_management()
    elif choice == "2":
        test_switching_logic()
    elif choice == "3":
        test_account_management()
        print("\n" + "=" * 50)
        test_switching_logic()
    else:
        print("Invalid choice. Running both tests...")
        test_account_management()
        print("\n" + "=" * 50)
        test_switching_logic()
    
    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()