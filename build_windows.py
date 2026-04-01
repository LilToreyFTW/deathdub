#!/usr/bin/env python3
"""
Windows Executable Builder v2.0
For Regenerative Addresses Tool - Educational Security Testing
"""

import os
import sys
import subprocess
import shutil
import zipfile
import tempfile

def create_windows_package():
    """Create a portable Windows package for v2.0"""
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    package_dir = os.path.join(temp_dir, "RegenerativeAddresses_v2")
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy all necessary files for v2.0
    files_to_copy = [
        "regenerative-addresses-new.py",
        "regenerative-addresses.py",  # Keep original as backup
        "kali_credential_obtainer.py", 
        "auto_updater.py",
        "proxy_manager.py",
        "users.json",
        "all_proxies.txt",
        "proxies.txt",
        "http_proxies.txt",
        "http_proxies2.txt",
        "socks4_proxies.txt",
        "socks4_proxies2.txt",
        "socks5_proxies.txt",
        "socks5_proxies2.txt",
        "WINDOWS_BUILD_SCRIPT.bat",
        "README_WINDOWS.md",
        "src",  # Include PHP directory
        "index.php"
    ]
    
    print("Creating Windows package v2.0...")
    
    for file in files_to_copy:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.copytree(file, os.path.join(package_dir, file))
            else:
                shutil.copy2(file, package_dir)
            print(f"Copied: {file}")
        else:
            print(f"Warning: {file} not found")
    
    # Create a Windows launcher for v2.0
    launcher_content = '''@echo off
cd /d "%~dp0"
echo Starting Regenerative Addresses Tool v2.0...
echo.
echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
echo   Regenerative Addresses Tool v2.0
echo   Educational Security Testing Tool
echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
echo.
python regenerative-addresses-new.py
if errorlevel 1 (
    echo.
    echo Error running v2.0, trying original version...
    python regenerative-addresses.py
)
pause
'''
    
    launcher_path = os.path.join(package_dir, "Run_RegenerativeAddresses_v2.bat")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Create PHP launcher
    php_launcher = '''@echo off
cd /d "%~dp0"
echo Starting PHP Web Interface...
echo.
echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
echo   Regenerative Addresses Tool - PHP Interface
echo   Educational Security Testing Tool
echo =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
echo.
echo Starting local PHP server...
echo Access: http://localhost:8000
echo Press Ctrl+C to stop server
echo.
cd src
python -m http.server 8000
pause
'''
    
    php_launcher_path = os.path.join(package_dir, "Start_PHP_Interface.bat")
    with open(php_launcher_path, 'w') as f:
        f.write(php_launcher)
    
    # Create README v2.0
    readme_content = '''# Regenerative Addresses Tool v2.0 - Windows Package

## NEW FEATURES v2.0:
- Completely rebuilt interface with modern GUI
- Enhanced PHP web interface integration
- Improved proxy management
- Better session handling
- Educational Kali tools integration
- HTML processing capabilities
- Auto-update functionality

## Installation:
1. Install Python 3.9+ from https://python.org
2. Extract this package to a folder
3. Run "Run_RegenerativeAddresses_v2.bat"

## Alternative Launch Options:
- Run "Start_PHP_Interface.bat" for web interface
- Run directly: python regenerative-addresses-new.py
- Use original version: python regenerative-addresses.py

## Default Login:
Username: admin
Password: admin

## Features:
- Link regeneration with 7 techniques
- 18,835+ proxy addresses  
- Kali Linux tools integration
- PHP web interface
- HTML processing and analysis
- Educational security testing
- Session management
- Auto-updater

## PHP Web Interface:
1. Run "Start_PHP_Interface.bat"
2. Open http://localhost:8000 in browser
3. Login with admin/admin

## Educational Purpose Only:
This tool is designed for legitimate security testing and educational purposes only.
'''
    
    readme_path = os.path.join(package_dir, "README_v2.txt")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    # Create ZIP package
    zip_path = "RegenerativeAddresses_v2_Windows_Package.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_path)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ Windows package v2.0 created: {zip_path}")
    print(f"Size: {os.path.getsize(zip_path) / 1024 / 1024:.1f} MB")
    print("\nTo use on Windows:")
    print("1. Extract the ZIP file")
    print("2. Install Python 3.9+")
    print("3. Run 'Run_RegenerativeAddresses_v2.bat'")
    print("4. Or try 'Start_PHP_Interface.bat' for web interface")
    
    return zip_path

def create_standalone_exe():
    """Try to create standalone executable with available tools"""
    
    # Try PyInstaller first
    try:
        print("Attempting PyInstaller build for v2.0...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--onefile", 
            "--windowed", 
            "--name", "RegenerativeAddresses_v2",
            "--add-data", "all_proxies.txt:.",
            "--add-data", "proxies.txt:.",
            "--add-data", "users.json:.",
            "--add-data", "kali_credential_obtainer.py:.",
            "--add-data", "auto_updater.py:.",
            "--add-data", "proxy_manager.py:.",
            "--add-data", "src:src",
            "--add-data", "index.php:.",
            "regenerative-addresses-new.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists("dist/RegenerativeAddresses_v2.exe"):
            print("✅ Windows .exe created with PyInstaller!")
            return "dist/RegenerativeAddresses_v2.exe"
        else:
            print(f"PyInstaller failed: {result.stderr}")
            
    except Exception as e:
        print(f"PyInstaller error: {e}")
    
    # Fallback to portable package
    print("\nFalling back to portable Windows package...")
    return create_windows_package()

if __name__ == "__main__":
    try:
        exe_path = create_standalone_exe()
        print(f"\n🎯 Build complete: {exe_path}")
        print("\n📋 Package Contents:")
        print("- RegenerativeAddresses Tool v2.0")
        print("- PHP Web Interface")
        print("- All proxy files")
        print("- Complete source code")
        print("- Installation instructions")
    except Exception as e:
        print(f"❌ Build failed: {e}")
        print("Please run the batch file on Windows instead.")
