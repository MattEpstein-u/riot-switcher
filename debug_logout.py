#!/usr/bin/env python3
"""
Debug script to test logout functionality without GUI
"""

from core.riot_client import RiotClient
import time

def test_logout():
    print("=== Riot Client Logout Test ===")
    
    rc = RiotClient()
    
    # Check initial status
    print(f"1. Riot Client running: {rc.is_running()}")
    
    if rc.is_running():
        current_user = rc.get_current_user()
        print(f"2. Current user: {current_user}")
        
        # Test logout
        print("\n3. Testing force logout...")
        success = rc.force_logout()
        print(f"   Logout successful: {success}")
        
        # Wait and check status again
        time.sleep(3)
        print(f"4. Riot Client running after logout: {rc.is_running()}")
        
        if not rc.is_running():
            print("   ✅ Client successfully terminated")
        else:
            print("   ❌ Client still running")
            
    else:
        print("2. No Riot Client running - testing session clearing...")
        success = rc.clear_current_session()
        print(f"   Session clearing successful: {success}")
        
    print("\n=== Test Complete ===")
    
def test_detection():
    print("=== Riot Client Detection Test ===")
    
    rc = RiotClient()
    
    print(f"System: {rc.system}")
    print(f"Config path: {rc.riot_paths['config']}")
    print(f"Install path: {rc.riot_paths['install']}")
    print(f"Running: {rc.is_running()}")
    
    processes = rc.get_running_processes()
    if processes:
        print("Running Riot processes:")
        for proc in processes:
            print(f"  - {proc['name']} (PID: {proc['pid']})")
    else:
        print("No Riot processes detected")
        
    current_user = rc.get_current_user()
    print(f"Current user: {current_user}")

if __name__ == "__main__":
    print("Choose test:")
    print("1. Detection test")
    print("2. Logout test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_detection()
    elif choice == "2":
        test_logout()
    else:
        print("Running both tests...")
        test_detection()
        print()
        test_logout()