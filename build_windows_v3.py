#!/usr/bin/env python3
"""
Windows Executable Builder v3.0
For Regenerative Addresses Tool Pro - Professional Security Protection
"""

import os
import sys
import subprocess
import shutil
import zipfile
import tempfile

def create_windows_package():
    """Create a portable Windows package for v3.0"""
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    package_dir = os.path.join(temp_dir, "RegenerativeAddressesPro_v3")
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy all necessary files for v3.0
    files_to_copy = [
        "regenerative-addresses-pro.py",
        "regenerative-addresses.py",  # Keep original as backup
        "kali_credential_obtainer.py", 
        "auto_updater.py",
        "proxy_manager.py",
        "security_scanner.py",  # NEW v3.0 security tools
        "system_hardener.py",  # NEW v3.0 hardening tools
        "networking_education.py",  # NEW v3.0 education module
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
        "README_REBUILD.md",
        "src",  # Include PHP directory
        "index.php",
        "api.php",  # NEW v3.0 API
        "src/controllers/coffee.php",  # NEW coffee controller
        "src/views/coffee.min.php"  # NEW coffee view
    ]
    
    print("Creating Windows package v3.0...")
    
    for file in files_to_copy:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.copytree(file, os.path.join(package_dir, file))
            else:
                shutil.copy2(file, package_dir)
            print(f"Copied: {file}")
        else:
            print(f"Warning: {file} not found")
    
    # Create a Windows launcher for v3.0
    launcher_content = '''@echo off
cd /d "%~dp0"
echo Starting Regenerative Addresses Tool Pro v3.0...
echo.
echo ===========================================
echo   Regenerative Addresses Tool Pro v3.0
echo   Professional Security Protection Tool
echo ===========================================
echo.
echo Features:
echo - Real Security Scanner and Protection
echo - System Hardening and Audit Tools
echo - Networking Security Education
echo - Professional Link Regeneration
echo - Enhanced Proxy Management
echo - PHP Web Interface Integration
echo.
python regenerative-addresses-pro.py
if errorlevel 1 (
    echo.
    echo Error running v3.0, trying original version...
    python regenerative-addresses.py
)
pause
'''
    
    launcher_path = os.path.join(package_dir, "Run_RegenerativeAddressesPro_v3.bat")
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    
    # Create PHP launcher
    php_launcher = '''@echo off
cd /d "%~dp0"
echo Starting PHP Web Interface v3.0...
echo.
echo ===========================================
echo   Regenerative Addresses Tool Pro v3.0
echo   PHP Web Interface with Security Features
echo ===========================================
echo.
echo Features:
echo - Professional Security Dashboard
echo - Real-time Vulnerability Scanning
echo - System Hardening Interface
echo - Networking Education Portal
echo - Security Reporting System
echo.
echo Starting local PHP server...
echo Access: http://localhost:8000
echo Press Ctrl+C to stop server
echo.
cd src
python -m http.server 8000
pause
'''
    
    php_launcher_path = os.path.join(package_dir, "Start_PHP_Interface_v3.bat")
    with open(php_launcher_path, 'w') as f:
        f.write(php_launcher)
    
    # Create README v3.0
    readme_content = '''# Regenerative Addresses Tool Pro v3.0 - Windows Package

## NEW FEATURES v3.0:
- 🛡️ Real Security Scanner and Protection Tools
- 🔧 System Hardening and Audit Utilities
- 🌐 Networking Security Education Module
- ☕ Buy Me a Coffee Support Tab
- 🚨 Real-time Protection Monitoring
- 📋 Professional Security Reporting
- 🎨 Enhanced Dark Theme Interface
- 💾 SQLite Database Integration

## SECURITY PROTECTION FEATURES:
- System vulnerability scanning with detailed analysis
- Password security strength assessment
- Network vulnerability detection and mapping
- System hardening for Linux and Windows
- Real-time threat detection and monitoring
- Professional security audit and reporting
- Educational networking security resources

## Installation:
1. Install Python 3.9+ from https://python.org
2. Extract this package to a folder
3. Run "Run_RegenerativeAddressesPro_v3.bat"

## Alternative Launch Options:
- Run "Start_PHP_Interface_v3.bat" for web interface
- Run directly: python regenerative-addresses-pro.py
- Use original version: python regenerative-addresses.py

## Default Login:
Username: admin
Password: admin

## Security Features:
- KEEP ME SAFE: Real security protection tools
- KEEP ME SAFE 2: Networking security education
- ☕ Coffee: Support development
- Professional vulnerability scanning
- System hardening and audit capabilities
- Real-time protection monitoring

## PHP Web Interface:
1. Run "Start_PHP_Interface_v3.bat"
2. Open http://localhost:8000 in browser
3. Login with admin/admin
4. Access all security features via web interface

## Professional Purpose:
This tool is designed for legitimate security testing, system protection, and educational purposes only.
All security features are white hat tools for protecting systems and users.

## Proxy Database:
- 7,419+ unique proxy addresses
- Multiple proxy types (HTTP, SOCKS4, SOCKS5)
- Professional proxy testing and management
- Real-time proxy validation
'''
    
    readme_path = os.path.join(package_dir, "README_v3.txt")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    # Create ZIP package
    zip_path = "RegenerativeAddressesPro_v3.0_Windows_Package.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arc_path)
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print(f"\n✅ Windows package v3.0 created: {zip_path}")
    print(f"Size: {os.path.getsize(zip_path) / 1024 / 1024:.1f} MB")
    print("\nTo use on Windows:")
    print("1. Extracts ZIP file")
    print("2. Install Python 3.9+")
    print("3. Run 'Run_RegenerativeAddressesPro_v3.bat'")
    print("4. Or try 'Start_PHP_Interface_v3.bat' for web interface")
    
    return zip_path

def create_standalone_exe():
    """Try to create standalone executable with available tools"""
    
    # Try PyInstaller first
    try:
        print("Attempting PyInstaller build for v3.0...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--onefile", 
            "--windowed", 
            "--name", "RegenerativeAddressesPro_v3",
            "--add-data", "all_proxies.txt:.",
            "--add-data", "proxies.txt:.",
            "--add-data", "users.json:.",
            "--add-data", "kali_credential_obtainer.py:.",
            "--add-data", "auto_updater.py:.",
            "--add-data", "proxy_manager.py:.",
            "--add-data", "security_scanner.py:.",  # NEW
            "--add-data", "system_hardener.py:.",  # NEW
            "--add-data", "networking_education.py:.",  # NEW
            "--add-data", "src:src",
            "--add-data", "index.php:.",
            "--add-data", "api.php:.",  # NEW
            "regenerative-addresses-pro.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0 and os.path.exists("dist/RegenerativeAddressesPro_v3.exe"):
            print("✅ Windows .exe created with PyInstaller!")
            return "dist/RegenerativeAddressesPro_v3.exe"
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
        print("- Regenerative Addresses Tool Pro v3.0")
        print("- Real Security Protection Tools")
        print("- System Hardening and Audit")
        print("- Networking Security Education")
        print("- PHP Web Interface with Security Dashboard")
        print("- All proxy files (7,419+ addresses)")
        print("- Complete source code")
        print("- Installation instructions")
    except Exception as e:
        print(f"❌ Build failed: {e}")
        print("Please run the batch file on Windows instead.")
