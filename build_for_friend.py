import os
import sys
import subprocess
import shutil

def build_executable():
    """Build a Windows executable using PyInstaller"""
    print("🔨 Building Riot Account Switcher executable...")
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # PyInstaller command with optimized settings
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=RiotAccountSwitcher",   # Executable name
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui", 
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=cryptography",
        "--hidden-import=psutil",
        "--hidden-import=yaml",
        "main.py"
    ]
    

    
    # Run PyInstaller
    try:
        print("🚀 Running PyInstaller...")
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            print("📁 Location: dist/RiotAccountSwitcher.exe")
            return True
        else:
            print("❌ Build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error during build: {e}")
        return False

def create_user_package():
    """Create a complete package for end users"""
    print("\n📦 Creating user package...")
    
    # Create distribution directory
    package_dir = "RiotAccountSwitcher_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy executable
    exe_source = "dist/RiotAccountSwitcher.exe"
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, package_dir)
        print("✅ Copied executable")
    else:
        print("❌ Executable not found! Run build first.")
        return False
    
    # Create user-friendly README
    create_user_readme(package_dir)
    
    # Create quick start batch file
    create_batch_file(package_dir)
    
    print(f"✅ Package ready: {package_dir}/")
    print("\n📋 Package contents:")
    for item in os.listdir(package_dir):
        print(f"   • {item}")
    
    return True

def create_user_readme(package_dir):
    """Create simple README for end users"""
    readme_content = """# 🎮 Riot Account Switcher

## 🚀 Quick Start (3 Steps!)

### 1. Run the App
• Double-click `RiotAccountSwitcher.exe`
• Windows might ask for permission - click "Allow"

### 2. Add Your Accounts
• Click "➕ Add" button
• Enter your Riot account details:
  - Display Name: Any name you want (e.g., "Main", "Smurf")
  - Username: Your Riot username/email
  - Password: Your account password
• Click "Add Account"
• Repeat for all your accounts

### 3. Set Up Each Account (One-time only)
• Select an account from the list
• Click "🔄 SWITCH"
• Riot Client will open to login screen
• **IMPORTANT**: Log in AND check "☑️ Stay logged in" box!
• Close Riot Client after successful login
• Click "💾 Backup" in the switcher app

### 🎉 Done! Future Account Switches Are Instant!

---

## 💡 How to Use Daily

1. **Open the app** (RiotAccountSwitcher.exe)
2. **Select account** from the list (✅ = Ready, ⚙️ = Needs setup)
3. **Click "🔄 SWITCH"** 
4. **Riot opens logged in** - no typing needed! 🚀

---

## 🔧 Troubleshooting

**"Account won't switch automatically"**
→ Make sure you checked "Stay logged in" during setup
→ Try the setup process again for that account

**"App says Riot Client not detected"**
→ Make sure Riot Games is installed normally
→ Try running as Administrator (right-click app → "Run as administrator")

**"Account shows ⚙️ instead of ✅"** 
→ This account needs first-time setup (see Step 3 above)

**"Switching is slow"**
→ This is normal for the first switch to each account
→ After setup, switches should be ~5 seconds

---

## 🛡️ Security

• All passwords are encrypted and stored locally
• No data is sent over the internet
• Your accounts are as safe as Riot's own "Stay logged in" feature

---

## 📞 Need Help?

If you're stuck:
1. Close both the switcher app and Riot Client
2. Run RiotAccountSwitcher.exe as Administrator
3. Try the setup process again
4. Check that "Stay logged in" is enabled in Riot settings

**Enjoy switching accounts instantly!** 🎮✨
"""
    
    with open(os.path.join(package_dir, "README.txt"), 'w') as f:
        f.write(readme_content)
    print("✅ Created user README")

def create_batch_file(package_dir):
    """Create a batch file for easy launching"""
    batch_content = """@echo off
echo 🎮 Starting Riot Account Switcher...
echo.
echo If Windows Defender blocks this, click "More info" then "Run anyway"
echo This is normal for new apps.
echo.
pause
RiotAccountSwitcher.exe
"""
    
    with open(os.path.join(package_dir, "START_HERE.bat"), 'w') as f:
        f.write(batch_content)
    print("✅ Created launch batch file")

def main():
    """Main build and package process"""
    print("🎮 Riot Account Switcher - Windows Package Builder")
    print("=" * 50)
    
    # Check if we're on the right system
    if sys.platform != "win32":
        print("⚠️  Warning: Building for Windows from non-Windows system")
        print("   The executable may not work properly.")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Step 1: Build executable
    print("\n🔨 STEP 1: Building executable...")
    if not build_executable():
        print("❌ Build failed. Cannot continue.")
        return
    
    # Step 2: Create user package
    print("\n📦 STEP 2: Creating user package...")
    if not create_user_package():
        print("❌ Package creation failed.")
        return
    
    # Step 3: Final instructions
    print("\n🎉 SUCCESS! Package ready for your friend!")
    print("=" * 50)
    print("📁 Send this folder to your friend: RiotAccountSwitcher_Package/")
    print("📋 They should:")
    print("   1. Extract/copy the folder to their computer")
    print("   2. Double-click START_HERE.bat (or RiotAccountSwitcher.exe)")
    print("   3. Follow the README.txt instructions")
    print("\n💡 The exe file is completely self-contained - no Python needed!")

if __name__ == "__main__":
    main()