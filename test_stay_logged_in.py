#!/usr/bin/env python3
"""
Test the "Stay Logged In" workflow
"""

from core.account_manager import AccountManager
from core.riot_client import RiotClient
import time

def test_stay_logged_in_workflow():
    print("=== Stay Logged In Workflow Test ===")
    print()
    
    rc = RiotClient()
    am = AccountManager()
    
    # Check current status
    print("🔍 Current Status:")
    print(f"   Riot Client running: {rc.is_running()}")
    print(f"   User logged in: {rc.is_logged_in()}")
    print(f"   Current user: {rc.get_current_user()}")
    print()
    
    # List existing accounts
    accounts = am.get_all_accounts()
    if accounts:
        print("📋 Saved Accounts:")
        for i, account in enumerate(accounts, 1):
            backup_path = rc._get_account_backup_path(account['display_name'])
            has_backup = "✅ Ready" if backup_path and os.path.exists(backup_path) else "⚠️ Needs setup"
            print(f"   {i}. {account['display_name']} ({account['username']}) - {has_backup}")
        print()
        
        # Test account switching workflow
        if len(accounts) >= 1:
            test_account = accounts[0]
            print(f"🧪 Testing workflow with: {test_account['display_name']}")
            print()
            
            # Get full account details
            full_account = am.get_account(test_account['id'])
            
            # Check if it has a backup
            backup_path = rc._get_account_backup_path(full_account['display_name'])
            
            if os.path.exists(backup_path):
                print("✅ This account has a saved session!")
                print("   Testing automatic switch...")
                
                choice = input("   Switch to this account? (y/N): ").lower().strip()
                if choice == 'y':
                    print("   Initiating switch...")
                    success = rc.switch_account(full_account)
                    if success:
                        print("   ✅ Switch completed!")
                        time.sleep(3)
                        print(f"   New status - Running: {rc.is_running()}, Logged in: {rc.is_logged_in()}")
                    else:
                        print("   ❌ Switch failed")
                
            else:
                print("⚠️  This account needs first-time setup")
                print("   Workflow:")
                print("   1. Run the GUI app: python main.py")
                print("   2. Select this account and click 'Quick Login Guide'")
                print("   3. Follow the setup instructions")
                print("   4. Remember to check 'Stay logged in'!")
                print()
                
                choice = input("   Start first-time setup now? (y/N): ").lower().strip()
                if choice == 'y':
                    print(f"   Starting Riot Client for {full_account['display_name']}...")
                    print(f"   Username to use: {full_account['username']}")
                    print("   ⚠️  Don't forget to check 'Stay logged in'!")
                    
                    rc.start_riot_client()
                    
                    print()
                    print("   After logging in successfully:")
                    print("   1. Close Riot Client") 
                    print("   2. Run: python create_backup_for_account.py")
                    print("   3. Or use the GUI 'Backup Current Session' button")
    else:
        print("❌ No accounts found!")
        print("   1. Run: python main.py")
        print("   2. Click 'Add Account' to create your first account")
        print("   3. Then run this test again")

def show_backup_info():
    print("=== Account Backup Information ===")
    print()
    
    am = AccountManager()
    rc = RiotClient()
    
    accounts = am.get_all_accounts()
    
    if not accounts:
        print("No accounts found.")
        return
        
    for account in accounts:
        print(f"📱 {account['display_name']} ({account['username']})")
        
        backup_path = rc._get_account_backup_path(account['display_name'])
        
        if os.path.exists(backup_path):
            # Get backup info
            info_file = os.path.join(backup_path, 'account_info.json')
            if os.path.exists(info_file):
                import json
                try:
                    with open(info_file, 'r') as f:
                        info = json.load(f)
                    print(f"   ✅ Backup exists")
                    print(f"   📅 Created: {info.get('backup_created', 'Unknown')}")
                    print(f"   💾 Size: {info.get('backup_size_mb', 'Unknown')} MB")
                    print(f"   🔧 Type: {info.get('session_type', 'Unknown')}")
                except:
                    print(f"   ✅ Backup exists (no details available)")
            else:
                print(f"   ✅ Backup exists (basic)")
                
            # Count files in backup
            try:
                import os
                file_count = sum([len(files) for r, d, files in os.walk(backup_path)])
                print(f"   📁 Files: {file_count}")
            except:
                pass
        else:
            print(f"   ❌ No backup - needs first-time setup")
            
        print()

def main():
    print("Riot Account Switcher - Stay Logged In Test")
    print("=" * 50)
    
    print("Choose test:")
    print("1. Test stay logged in workflow")
    print("2. Show backup information")
    print("3. Both")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        test_stay_logged_in_workflow()
    elif choice == "2":
        show_backup_info()
    elif choice == "3":
        show_backup_info()
        print("\n" + "=" * 50)
        test_stay_logged_in_workflow()
    else:
        print("Invalid choice. Running workflow test...")
        test_stay_logged_in_workflow()

if __name__ == "__main__":
    import os
    main()