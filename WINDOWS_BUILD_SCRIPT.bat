@echo off
echo Building Regenerative Addresses Windows Executable...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM Install PyInstaller
echo Installing PyInstaller...
python -m pip install pyinstaller

REM Build the executable
echo Building Windows executable...
python -m PyInstaller --onefile --windowed --name "RegenerativeAddresses" regenerative-addresses.py

REM Check if build was successful
if exist "dist\RegenerativeAddresses.exe" (
    echo.
    echo SUCCESS! Windows executable created:
    echo dist\RegenerativeAddresses.exe
    echo.
    echo Size: 
    dir "dist\RegenerativeAddresses.exe" | find "RegenerativeAddresses.exe"
    echo.
    echo You can now run RegenerativeAddresses.exe on any Windows system
) else (
    echo ERROR: Build failed. Check the output above for errors.
)

pause
