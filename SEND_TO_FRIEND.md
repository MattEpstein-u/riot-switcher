# 🎮 Riot Account Switcher - For Your Friend

## 📦 Easy 3-Step Setup for Windows (No Python Required!)

### What Your Friend Gets:
- ✅ **One-click account switching** (5 seconds vs typing passwords)
- ✅ **Persistent sessions** (works for days without re-login)
- ✅ **Secure local storage** (passwords encrypted, never sent online)
- ✅ **No installation needed** (just run the .exe file)

---

## 🚀 How to Build & Send

### Step 1: Build the Executable (On Your Machine)
```bash
# In your riot-switcher folder
python build_for_friend.py
```

This creates: `RiotAccountSwitcher_Package/` folder with everything your friend needs.

### Step 2: Send to Your Friend
**Zip and send the entire `RiotAccountSwitcher_Package/` folder**

Contents:
- `RiotAccountSwitcher.exe` - The main app
- `README.txt` - Simple instructions  
- `START_HERE.bat` - Easy launcher

### Step 3: Your Friend's Setup (Super Simple!)

#### First Run:
1. **Extract** the folder anywhere on their PC
2. **Double-click** `START_HERE.bat` (or `RiotAccountSwitcher.exe`)
3. **Windows Defender** might warn about unknown app:
   - Click "More info" → "Run anyway" 
   - This is normal for new apps!

#### Add Accounts (One-time):
1. **Click "➕ Add"** in the app
2. **Enter account info**:
   - Display Name: "Main Account" (or whatever)
   - Username: their Riot username/email  
   - Password: their password
3. **Repeat** for each account they want

#### Setup Each Account (One-time):
1. **Select account** → Click "🔄 SWITCH"  
2. **Riot opens** → Log in normally
3. **✅ CRITICAL: Check "Stay logged in" box!**
4. **Close Riot** after successful login
5. **Click "💾 Backup"** in the switcher app
6. **Done!** That account is now ready for instant switching

#### Daily Use (The Magic!):
1. **Open app** → **Select account** → **Click "🔄 SWITCH"**
2. **Riot opens already logged in!** 🚀
3. No more typing passwords every time!

---

## 🛠️ If Your Friend Has Issues

### Common Problems:

**"Windows won't let me run it"**
→ Right-click the .exe → "Run as administrator"  
→ Or: Windows Security → Allow app

**"Account won't switch automatically"**  
→ They forgot to check "Stay logged in" during setup
→ Redo the setup for that account

**"App can't find Riot Client"**
→ Make sure Riot Games is installed normally (default location)
→ Try running app as administrator

**"Switching is slow"**
→ Normal for first-time setup of each account
→ After setup: switches should be ~5 seconds

---

## 💡 Pro Tips for Your Friend

### Account Management:
- **✅ Green accounts** = Ready for instant switching
- **⚙️ Orange accounts** = Need setup (follow setup steps)
- **Hover over accounts** for status details

### Best Practices:
- **Keep "Stay logged in" checked** in Riot for all accounts
- **Don't log out manually** in Riot (breaks the saved session)
- **If session expires**: Just redo the setup for that account

### Troubleshooting:
- **App shows account status** at the top (Online/Offline/Error)
- **Green button** = everything ready to switch
- **Red/Orange status** = something needs attention

---

## 🎉 What Your Friend Will Love

- **5-second account switches** instead of typing passwords
- **No more "forgot which email I used"** - all accounts saved
- **Sessions persist for weeks** until manually logged out
- **Clean, simple interface** - just click and go!

**Your friend will thank you for this time-saver!** ⏰→⚡

---

## 📋 Quick Checklist for You

Before sending:
- [ ] Run `python build_for_friend.py`  
- [ ] Check that `RiotAccountSwitcher_Package/` folder contains:
  - [ ] `RiotAccountSwitcher.exe`
  - [ ] `README.txt`  
  - [ ] `START_HERE.bat`
- [ ] Zip the folder
- [ ] Send to friend with message: "Run START_HERE.bat first!"

**That's it! Your friend gets a professional account switcher with zero technical setup.** 🚀