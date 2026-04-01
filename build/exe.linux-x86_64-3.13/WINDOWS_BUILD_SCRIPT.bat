@echo off
echo Building Regenerative Addresses Tool Pro v3.0 Windows Executable...
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

REM Build executable for v3.0
echo Building Regenerative Addresses Tool Pro v3.0...
python -m PyInstaller --onefile --windowed --name "RegenerativeAddressesPro_v3" ^
    --add-data "security_scanner.py:." ^
    --add-data "system_hardener.py:." ^
    --add-data "networking_education.py:." ^
    --add-data "api.php:." ^
    --add-data "src:src" ^
    --add-data "all_proxies.txt:." ^
    --add-data "proxies.txt:." ^
    --add-data "users.json:." ^
    regenerative-addresses-pro.py

REM Check if build was successful
if exist "dist\RegenerativeAddressesPro_v3.exe" (
    echo.
    echo SUCCESS! Regenerative Addresses Tool Pro v3.0 created:
    echo dist\RegenerativeAddressesPro_v3.exe
    echo.
    echo Features:
    echo - Real Security Scanner and Protection Tools
    echo - System Hardening and Audit Utilities
    echo - Networking Security Education Module
    echo - Professional Vulnerability Assessment
    echo - Enhanced Proxy Management (7,419+ addresses)
    echo - PHP Web Interface with Security Dashboard
    echo - Professional Dark Theme GUI
    echo.
    echo Size:
    dir "dist\RegenerativeAddressesPro_v3.exe" | find "RegenerativeAddressesPro_v3.exe"
    echo.
    echo You can now run RegenerativeAddressesPro_v3.exe on any Windows system
    echo.
    echo To create Windows package:
    echo 1. Create RegenerativeAddressesPro_v3 folder
    echo 2. Copy RegenerativeAddressesPro_v3.exe to folder
    echo 3. Copy all .txt, .py, and src files
    echo 4. Create launchers and documentation
) else (
    echo.
    echo ERROR: Build failed!
    echo Please check error messages above.
    echo Make sure all required files are present:
    echo - regenerative-addresses-pro.py
    echo - security_scanner.py
    echo - system_hardener.py
    echo - networking_education.py
    echo - api.php
    echo - src\ folder
    echo - all_proxies.txt
    echo - proxies.txt
    echo - users.json
)

pause
