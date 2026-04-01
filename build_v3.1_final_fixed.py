#!/usr/bin/env python3
"""
Build Script for Regenerative Addresses Tool Pro v3.1
Creates Windows and Linux executable builds and releases
"""

import os
import sys
import subprocess
import shutil
import zipfile
import platform
from pathlib import Path

def create_build_directory():
    """Create build directory"""
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    return build_dir

def install_dependencies():
    """Install PyInstaller and dependencies"""
    print("🔧 Installing dependencies...")
    
    # Install PyInstaller with system override
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "pyinstaller"], check=True)
    
    # Install required packages
    requirements = [
        "requests>=2.31.0",
        "Pillow>=10.0.0",
        "python-dotenv>=1.0.0",
        "psutil>=5.9.0",
        "cryptography>=41.0.0"
    ]
    
    for req in requirements:
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", req], check=True)

def create_requirements_file():
    """Create requirements.txt file"""
    requirements_content = '''requests>=2.31.0
Pillow>=10.0.0
python-dotenv>=1.0.0
psutil>=5.9.0
cryptography>=41.0.0
'''
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("✅ Created requirements.txt")

def create_spec_file():
    """Create PyInstaller spec file"""
    current_platform = platform.system()
    icon_path = 'icon.ico' if current_platform == 'Windows' else None
    version_path = 'version_info.txt' if current_platform == 'Windows' else None
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import platform

block_cipher = None

a = Analysis(
    ['regenerative-addresses-pro.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('requirements.txt', '.'),
        ('RELEASE_NOTES_v3.1.md', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'sqlite3',
        'hashlib',
        'uuid',
        'datetime',
        'threading',
        'socket',
        'subprocess',
        'webbrowser',
        'ssl',
        'json',
        'base64',
        'time',
        'os',
        'sys',
        'random',
        'string',
        'ipaddress',
        're',
        'io',
        'psutil',
        'cryptography'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RegenerativeAddressesToolPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={repr(icon_path)},
    version={repr(version_path)}
)
'''
    
    with open('regenerative-addresses-pro.spec', 'w') as f:
        f.write(spec_content)

def create_version_info():
    """Create version info file for Windows"""
    if platform.system() == 'Windows':
        version_info = '''
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx

VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(3, 1, 0, 0),
prodvers=(3, 1, 0, 0),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'LilToreyFTW'),
    StringStruct(u'FileDescription', u'Regenerative Addresses Tool Pro v3.1'),
    StringStruct(u'FileVersion', u'3.1.0.0'),
    StringStruct(u'InternalName', u'RegenerativeAddressesToolPro'),
    StringStruct(u'LegalCopyright', u'Copyright © 2026 LilToreyFTW'),
    StringStruct(u'OriginalFilename', u'RegenerativeAddressesToolPro.exe'),
    StringStruct(u'ProductName', u'Regenerative Addresses Tool Pro'),
    StringStruct(u'ProductVersion', u'3.1.0.0')])
  ]), 
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
        
        with open('version_info.txt', 'w') as f:
            f.write(version_info)

def create_icon():
    """Create icon file for Windows"""
    if platform.system() == 'Windows':
        # Create a simple icon placeholder
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            # Draw a simple icon
            draw.ellipse([20, 20, 236, 236], fill=(70, 130, 180, 255))
            draw.text([50, 100], "RAT", fill=(255, 255, 255, 255))
            img.save('icon.ico')
        except:
            print("⚠️ Could not create icon file")

def build_executable():
    """Build executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # Create requirements file
    create_requirements_file()
    
    # Create spec file
    create_spec_file()
    
    # Create version info
    create_version_info()
    
    # Create icon
    create_icon()
    
    # Build executable using spec file only
    subprocess.run([sys.executable, "-m", "PyInstaller", 
                   "regenerative-addresses-pro.spec"], check=True)

def create_package():
    """Create distribution package"""
    print("📦 Creating package...")
    
    build_dir = create_build_directory()
    
    # Determine platform
    current_platform = platform.system().lower()
    if current_platform == 'windows':
        platform_name = 'windows'
        exe_name = 'RegenerativeAddressesToolPro.exe'
    elif current_platform == 'linux':
        platform_name = 'linux'
        exe_name = 'RegenerativeAddressesToolPro'
    else:
        print(f"❌ Unsupported platform: {current_platform}")
        return None
    
    # Create package directory
    package_dir = build_dir / f"RegenerativeAddressesToolPro-v3.1-{platform_name}"
    package_dir.mkdir(exist_ok=True)
    
    # Copy executable
    dist_dir = Path("dist")
    exe_path = dist_dir / exe_name
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir / exe_name)
        print(f"✅ Copied {exe_name}")
    else:
        print(f"❌ Executable not found: {exe_path}")
        return None
    
    # Copy additional files
    additional_files = [
        'README.md',
        'requirements.txt',
        'RELEASE_NOTES_v3.1.md'
    ]
    
    for file_name in additional_files:
        src_path = Path(file_name)
        if src_path.exists():
            shutil.copy2(src_path, package_dir / file_name)
            print(f"✅ Copied {file_name}")
        else:
            print(f"⚠️ File not found: {file_name}")
    
    # Create docs directory
    docs_dir = package_dir / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Create installation script
    if current_platform == 'windows':
        install_script = '''@echo off
echo Installing Regenerative Addresses Tool Pro v3.1...
echo.
echo Please wait while the application starts...
echo.
start "" "RegenerativeAddressesToolPro.exe"
echo.
echo Application started successfully!
pause
'''
        with open(package_dir / 'run.bat', 'w') as f:
            f.write(install_script)
    else:
        install_script = '''#!/bin/bash
echo "Installing Regenerative Addresses Tool Pro v3.1..."
echo
echo "Please wait while the application starts..."
echo
chmod +x RegenerativeAddressesToolPro
./RegenerativeAddressesToolPro
echo
echo "Application started successfully!"
read -p "Press Enter to continue..."
'''
        with open(package_dir / 'run.sh', 'w') as f:
            f.write(install_script)
        os.chmod(package_dir / 'run.sh', 0o755)
    
    # Create ZIP archive
    zip_name = f"RegenerativeAddressesToolPro-v3.1-{platform_name}.zip"
    zip_path = build_dir / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Created {zip_name}")
    return zip_path

def create_release_notes():
    """Create release notes for v3.1"""
    release_notes = '''# Regenerative Addresses Tool Pro v3.1 Release Notes

## 🚀 New Features in v3.1

### 🤖 AI Integration
- AI-powered link generation algorithms
- Machine learning for proxy optimization
- Intelligent VPN server selection
- Predictive performance analytics

### 🔐 Enhanced Security
- Advanced threat detection
- Behavioral analysis
- Predictive security measures
- Enhanced encryption algorithms

### 🎨 UI Improvements
- Modern dark theme
- Real-time status indicators
- Enhanced user experience
- Responsive design

### 🐳 Docker Enhancements
- Optimized container images
- Automated deployment
- Health monitoring
- Multi-platform support

## 🛠️ Installation

### Windows
1. Extract the ZIP file
2. Run `RegenerativeAddressesToolPro.exe` or `run.bat`
3. Follow the on-screen instructions

### Linux
1. Extract the ZIP file
2. Run `./run.sh` or `./RegenerativeAddressesToolPro`
3. Follow the on-screen instructions

## 📊 System Requirements

### Windows
- Windows 10 or later
- 4GB RAM minimum
- 100MB disk space
- Network connection

### Linux
- Ubuntu 18.04+ / CentOS 7+ / Debian 10+
- 4GB RAM minimum
- 100MB disk space
- Network connection

## 🔗 Links

- GitHub Repository: https://github.com/LilToreyFTW/deathdub
- Documentation: https://github.com/LilToreyFTW/deathdub/wiki
- Issues: https://github.com/LilToreyFTW/deathdub/issues
- Discussions: https://github.com/LilToreyFTW/deathdub/discussions

---
**Release Date**: April 1, 2026
**Version**: 3.1.0
**Status**: Production Ready
'''
    
    with open('RELEASE_NOTES_v3.1.md', 'w') as f:
        f.write(release_notes)
    
    print("✅ Created release notes")

def cleanup():
    """Clean up build artifacts"""
    print("🧹 Cleaning up...")
    
    # Remove build artifacts
    artifacts = [
        'build',
        'dist',
        'regenerative-addresses-pro.spec',
        'version_info.txt',
        'icon.ico',
        '__pycache__'
    ]
    
    for artifact in artifacts:
        artifact_path = Path(artifact)
        if artifact_path.exists():
            if artifact_path.is_dir():
                shutil.rmtree(artifact_path)
            else:
                artifact_path.unlink()
            print(f"✅ Removed {artifact}")

def main():
    """Main build process"""
    print("🚀 Building Regenerative Addresses Tool Pro v3.1")
    print("=" * 50)
    
    try:
        # Create release notes
        create_release_notes()
        
        # Build executable
        build_executable()
        
        # Create package
        package_path = create_package()
        
        if package_path:
            print(f"\n✅ Build completed successfully!")
            print(f"📦 Package created: {package_path}")
            print(f"📊 Package size: {package_path.stat().st_size / (1024*1024):.1f} MB")
        else:
            print("\n❌ Build failed!")
            return False
        
        # Clean up
        cleanup()
        
        print("\n🎉 Build process completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
