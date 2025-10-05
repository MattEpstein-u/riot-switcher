#!/usr/bin/env python3
"""
Alternative build script using auto-py-to-exe for easier GUI-based building
"""

import subprocess
import sys
import os

def install_build_tools():
    """Install the required build tools"""
    print("Installing build tools...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "auto-py-to-exe", "pyinstaller"])
        print("✅ Build tools installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install build tools")
        return False

def build_with_auto_py_to_exe():
    """Launch auto-py-to-exe GUI for easier building"""
    print("\n🚀 Launching auto-py-to-exe GUI...")
    print("Configure these settings in the GUI:")
    print("  1. Script Location: main.py")
    print("  2. Onefile: One File")
    print("  3. Console Window: Window Based (hide the console)")
    print("  4. Icon: (optional - add a .ico file)")
    print("  5. Additional Files: (none needed)")
    print("  6. Click 'CONVERT .PY TO .EXE'")
    print("\n" + "="*50)
    
    try:
        subprocess.run([sys.executable, "-m", "auto_py_to_exe"])
    except KeyboardInterrupt:
        print("\n👋 Build cancelled by user")
    except Exception as e:
        print(f"❌ Error launching auto-py-to-exe: {e}")

def build_with_pyinstaller():
    """Build directly with PyInstaller using our spec file"""
    print("\n🔧 Building with PyInstaller...")
    try:
        subprocess.check_call(["pyinstaller", "RiotAccountSwitcher.spec", "--clean"])
        print("✅ Build completed!")
        print("📁 Executable created in: dist/RiotAccountSwitcher.exe")
        return True
    except subprocess.CalledProcessError:
        print("❌ Build failed")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return build_with_pyinstaller()

def main():
    print("🎮 Riot Account Switcher - Build Tool")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        print("Please run this from the riot-switcher directory")
        return
    
    print("Choose build method:")
    print("1. Auto-py-to-exe (GUI - easier)")
    print("2. PyInstaller (command line - faster)")
    print("3. Install build tools only")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        if install_build_tools():
            build_with_auto_py_to_exe()
    elif choice == "2":
        if install_build_tools():
            build_with_pyinstaller()
    elif choice == "3":
        install_build_tools()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()