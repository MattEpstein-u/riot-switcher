@echo off
title Riot Account Switcher
echo.
echo ========================================
echo    🎮 Riot Account Switcher v1.0
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if the executable exists
if not exist "RiotAccountSwitcher.exe" (
    echo ❌ ERROR: RiotAccountSwitcher.exe not found!
    echo.
    echo Make sure you're running this from the correct folder.
    echo The folder should contain:
    echo   - RiotAccountSwitcher.exe
    echo   - This batch file
    echo.
    pause
    exit /b 1
)

REM Run the application
start "" "RiotAccountSwitcher.exe"

REM Optional: Keep window open for any error messages
timeout /t 2 /nobreak > nul
echo ✅ Application launched successfully!
echo.
echo 💡 Tips for first-time use:
echo   1. Add your Riot accounts using the '+ Add' button
echo   2. Always check 'Stay logged in' when setting up accounts
echo   3. Use 'Setup Guide' for step-by-step instructions
echo.
echo You can close this window now.
echo.
pause