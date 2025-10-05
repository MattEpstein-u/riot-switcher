# Riot Account Switcher - Quick Distribution Package

## For the Developer (You)

### Building the Executable:

#### Option 1: Simple Command Line Build
```bash
# Install build tools
pip install pyinstaller

# Build the executable
pyinstaller RiotAccountSwitcher.spec --clean
```

#### Option 2: GUI-Based Build (Easier)
```bash
# Install GUI build tool
pip install auto-py-to-exe

# Launch GUI builder
python build_exe.py
# Choose option 1, then configure in the GUI
```

#### Option 3: Windows Batch Script
```cmd
# Just double-click: build.bat
# It will do everything automatically
```

### Creating Distribution Package:

1. **Build the executable** (using any method above)
2. **Create a distribution folder** with:
   ```
   RiotAccountSwitcher_v1.0/
   ├── RiotAccountSwitcher.exe    (Main program)
   ├── START_HERE.bat             (Easy launcher)
   ├── USER_GUIDE.txt             (Instructions)
   └── README.txt                 (Quick start)
   ```
3. **Zip the folder** and send to your friend!

## For the End User (Your Friend)

### Installation:
1. **Extract the zip file** to any folder (e.g., Desktop)
2. **Double-click `START_HERE.bat`** to launch the app
3. That's it! No Python or additional software needed.

### First Use:
1. **Add accounts**: Click the "➕ Add" button
2. **Follow setup guide**: Click "🚀 Setup Guide" for each account
3. **Important**: Always check "✅ Stay logged in" in Riot Client!

### Daily Use:
- Select account → Click "🔄 SWITCH" → Instant login! 🚀

---

**The app is completely portable - just copy the folder anywhere and it works!**