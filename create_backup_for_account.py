#!/usr/bin/env python3
"""
Quick utility to backup current session for an account
"""

from core.account_manager import AccountManager
from core.riot_client import RiotClient

def create_backup():
    print("=== Create Session Backup ===")
    print()
    
    rc = RiotClient()
    am = AccountManager()
    
    # Check if logged in
    if not rc.is_logged_in():
        print("❌ No active session found!")
        print("   Please:")
        print("   1. Log into Riot Client")
        print("   2. Make sure 'Stay logged in' is checked")
        print("   3. Complete the login process")
        print("   4. Run this script again")
        return
        
    print("✅ Active session detected!")
    print(f"   Status: {rc.get_current_user()}")
    print()
    
    # List accounts
    accounts = am.get_all_accounts()
    
    if not accounts:
        print("❌ No accounts found!")
        print("   Please add accounts first using the main GUI (python main.py)")
        return
        
    print("📋 Available accounts:")
    for i, account in enumerate(accounts, 1):
        print(f"   {i}. {account['display_name']} ({account['username']})")
        
    print()
    
    # Let user choose account
    if len(accounts) == 1:
        selected_account = accounts[0]
        print(f"🎯 Auto-selected: {selected_account['display_name']}")
    else:
        try:
            choice = int(input("Select account number: ")) - 1
            if 0 <= choice < len(accounts):
                selected_account = accounts[choice]
            else:
                print("❌ Invalid selection")
                return
        except ValueError:
            print("❌ Invalid input")
            return
            
    # Get full account details
    full_account = am.get_account(selected_account['id'])
    
    print(f"📦 Creating backup for {full_account['display_name']}...")
    
    # Create backup
    success = rc.backup_account_session(full_account)
    
    if success:
        print("✅ Backup created successfully!")
        print()
        print("🎉 This account is now ready for automatic switching!")
        print("   You can use the GUI to switch between accounts instantly.")
        
        # Mark as used
        am.mark_account_used(full_account['id'])
        
    else:
        print("❌ Backup failed!")
        print("   Check the error messages above for details.")

if __name__ == "__main__":
    create_backup()