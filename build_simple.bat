@echo off
echo 🎮 Riot Account Switcher - Build for Friend
echo ==========================================
echo.
echo This will create a Windows .exe file that your friend can run
echo without installing Python or any dependencies.
echo.
pause

echo 📦 Installing build tools...
pip install pyinstaller

echo 🔨 Building executable (simple version without icon)...
pyinstaller --onefile --windowed --name=RiotAccountSwitcher main.py

echo 📂 Creating user package...
python build_for_friend.py

echo.
echo ✅ DONE! 
echo 📁 Send this folder to your friend: RiotAccountSwitcher_Package\
echo 💡 Tell them to run "START_HERE.bat" first
echo.
pause