@echo off
echo ===============================================
echo    Riot Account Switcher - Build Script
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Installing build dependencies...
pip install -r requirements-build.txt
if errorlevel 1 (
    echo ERROR: Failed to install build dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing app dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install app dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller RiotAccountSwitcher.spec --clean
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Creating distribution folder...
if not exist "distribution" mkdir distribution
copy "dist\RiotAccountSwitcher.exe" "distribution\"
copy "README.md" "distribution\README.txt"

echo.
echo ===============================================
echo           BUILD COMPLETED SUCCESSFULLY!
echo ===============================================
echo.
echo The executable is ready in the 'distribution' folder:
echo - RiotAccountSwitcher.exe  (Main application)
echo - README.txt               (Instructions)
echo.
echo You can now zip the 'distribution' folder and send it to your friend!
echo.
pause