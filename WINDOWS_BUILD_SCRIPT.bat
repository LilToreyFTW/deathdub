@echo off
echo Building Regenerative Addresses Tool Pro v3.1.0 Windows Executable...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install pyinstaller
python -m pip install requests>=2.31.0
python -m pip install Pillow>=10.0.0
python -m pip install python-dotenv>=1.0.0
python -m pip install psutil>=5.9.0
python -m pip install cryptography>=41.0.0

REM Create requirements.txt
echo Creating requirements.txt...
echo requests>=2.31.0 > requirements.txt
echo Pillow>=10.0.0 >> requirements.txt
echo python-dotenv>=1.0.0 >> requirements.txt
echo psutil>=5.9.0 >> requirements.txt
echo cryptography>=41.0.0 >> requirements.txt

REM Create release notes
echo Creating release notes...
echo # Regenerative Addresses Tool Pro v3.1.0 Release Notes > RELEASE_NOTES_v3.1.md
echo. >> RELEASE_NOTES_v3.1.md
echo ## 🚀 New Features in v3.1.0 >> RELEASE_NOTES_v3.1.md
echo. >> RELEASE_NOTES_v3.1.md
echo ### 🤖 AI Integration >> RELEASE_NOTES_v3.1.md
echo - AI-powered link generation algorithms >> RELEASE_NOTES_v3.1.md
echo - Machine learning for proxy optimization >> RELEASE_NOTES_v3.1.md
echo - Intelligent VPN server selection >> RELEASE_NOTES_v3.1.md
echo - Predictive performance analytics >> RELEASE_NOTES_v3.1.md
echo. >> RELEASE_NOTES_v3.1.md
echo ### 🔐 Enhanced Security >> RELEASE_NOTES_v3.1.md
echo - Advanced threat detection >> RELEASE_NOTES_v3.1.md
echo - Behavioral analysis >> RELEASE_NOTES_v3.1.md
echo - Predictive security measures >> RELEASE_NOTES_v3.1.md
echo - Enhanced encryption algorithms >> RELEASE_NOTES_v3.1.md

REM Create version info
echo Creating version info...
echo VSVersionInfo( > version_info.txt
echo   ffi=FixedFileInfo( >> version_info.txt
echo   filevers=(3, 1, 0, 0), >> version_info.txt
echo   prodvers=(3, 1, 0, 0), >> version_info.txt
echo   mask=0x3f, >> version_info.txt
echo   flags=0x0, >> version_info.txt
echo   OS=0x4, >> version_info.txt
echo   fileType=0x1, >> version_info.txt
echo   subtype=0x0, >> version_info.txt
echo   date=(0, 0) >> version_info.txt
echo   ), >> version_info.txt
echo   kids=[ >> version_info.txt
echo   StringFileInfo( >> version_info.txt
echo   [ >> version_info.txt
echo   StringTable( >> version_info.txt
echo   u'040904B0', >> version_info.txt
echo   [StringStruct(u'CompanyName', u'LilToreyFTW'), >> version_info.txt
echo   StringStruct(u'FileDescription', u'Regenerative Addresses Tool Pro v3.1.0'), >> version_info.txt
echo   StringStruct(u'FileVersion', u'3.1.0.0'), >> version_info.txt
echo   StringStruct(u'InternalName', u'RegenerativeAddressesToolPro'), >> version_info.txt
echo   StringStruct(u'LegalCopyright', u'Copyright © 2026 LilToreyFTW'), >> version_info.txt
echo   StringStruct(u'OriginalFilename', u'RegenerativeAddressesToolPro.exe'), >> version_info.txt
echo   StringStruct(u'ProductName', u'Regenerative Addresses Tool Pro'), >> version_info.txt
echo   StringStruct(u'ProductVersion', u'3.1.0.0')]) >> version_info.txt
echo   ]), >> version_info.txt
echo   VarFileInfo([VarStruct(u'Translation', [1033, 1200])]) >> version_info.txt
echo   ] >> version_info.txt
echo   ) >> version_info.txt

REM Create icon (if PIL is available)
echo Creating icon...
python -c "
try:
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 236, 236], fill=(70, 130, 180, 255))
    draw.text([50, 100], 'RAT', fill=(255, 255, 255, 255))
    img.save('icon.ico')
    print('Icon created successfully')
except Exception as e:
    print(f'Could not create icon: {e}')
"

REM Build executable for v3.1.0
echo Building Regenerative Addresses Tool Pro v3.1.0...
python -m PyInstaller --onefile --windowed --name "RegenerativeAddressesToolPro" ^
    --icon=icon.ico ^
    --version-file=version_info.txt ^
    --add-data "README.md;." ^
    --add-data "requirements.txt;." ^
    --add-data "RELEASE_NOTES_v3.1.md;." ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=tkinter.scrolledtext ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.simpledialog ^
    --hidden-import=PIL ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ImageTk ^
    --hidden-import=requests ^
    --hidden-import=sqlite3 ^
    --hidden-import=hashlib ^
    --hidden-import=uuid ^
    --hidden-import=datetime ^
    --hidden-import=threading ^
    --hidden-import=socket ^
    --hidden-import=subprocess ^
    --hidden-import=webbrowser ^
    --hidden-import=ssl ^
    --hidden-import=json ^
    --hidden-import=base64 ^
    --hidden-import=time ^
    --hidden-import=os ^
    --hidden-import=sys ^
    --hidden-import=random ^
    --hidden-import=string ^
    --hidden-import=ipaddress ^
    --hidden-import=re ^
    --hidden-import=io ^
    --hidden-import=psutil ^
    --hidden-import=cryptography ^
    regenerative-addresses-pro.py

REM Check if build was successful
if exist "dist\RegenerativeAddressesToolPro.exe" (
    echo.
    echo SUCCESS! Regenerative Addresses Tool Pro v3.1.0 created:
    echo dist\RegenerativeAddressesToolPro.exe
    echo.
    echo 🤖 AI-Powered Features:
    echo - AI-powered link generation algorithms
    echo - Machine learning for proxy optimization
    echo - Intelligent VPN server selection
    echo - Predictive performance analytics
    echo - Advanced threat detection
    echo - Behavioral analysis
    echo - Enhanced encryption algorithms
    echo - Modern dark theme UI
    echo - Real-time monitoring
    echo - Docker integration
    echo.
    echo 🔐 Security Enhancements:
    echo - SHA-256 password hashing
    echo - Advanced threat detection
    echo - Behavioral security analysis
    echo - Predictive security measures
    echo - Enhanced encryption algorithms
    echo.
    echo 🌐 VPN & Networking:
    echo - Real WireGuard implementation
    echo - C-based networking calls
    echo - Docker containerization
    echo - Advanced security features
    echo - Custom image integration
    echo.
    echo 📊 Size and Information:
    dir "dist\RegenerativeAddressesToolPro.exe" | find "RegenerativeAddressesToolPro.exe"
    echo.
    echo 📦 Creating Windows package...
    if not exist "build" mkdir build
    if not exist "build\RegenerativeAddressesToolPro-v3.1-windows" mkdir build\RegenerativeAddressesToolPro-v3.1-windows
    
    REM Copy files to package directory
    copy "dist\RegenerativeAddressesToolPro.exe" "build\RegenerativeAddressesToolPro-v3.1-windows\"
    copy "README.md" "build\RegenerativeAddressesToolPro-v3.1-windows\" >nul 2>&1
    copy "requirements.txt" "build\RegenerativeAddressesToolPro-v3.1-windows\"
    copy "RELEASE_NOTES_v3.1.md" "build\RegenerativeAddressesToolPro-v3.1-windows\"
    
    REM Create run.bat
    echo @echo off > "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo echo Installing Regenerative Addresses Tool Pro v3.1.0... >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo echo. >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo echo Please wait while the application starts... >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo echo. >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo start "" "RegenerativeAddressesToolPro.exe" >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo echo. >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo echo Application started successfully! >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    echo pause >> "build\RegenerativeAddressesToolPro-v3.1-windows\run.bat"
    
    REM Create ZIP package
    echo Creating ZIP package...
    cd build
    if exist "RegenerativeAddressesToolPro-v3.1-windows.zip" del "RegenerativeAddressesToolPro-v3.1-windows.zip"
    powershell -command "Compress-Archive -Path 'RegenerativeAddressesToolPro-v3.1-windows' -DestinationPath 'RegenerativeAddressesToolPro-v3.1-windows.zip'"
    cd ..
    
    echo.
    echo 🎉 Package created successfully!
    echo 📦 Package: build\RegenerativeAddressesToolPro-v3.1-windows.zip
    echo 🚀 Ready for release!
    echo.
    echo You can now:
    echo 1. Upload RegenerativeAddressesToolPro-v3.1-windows.zip to GitHub releases
    echo 2. Run RegenerativeAddressesToolPro.exe on any Windows system
    echo 3. Use run.bat for easy launcher
    echo.
    echo 🔗 GitHub: https://github.com/LilToreyFTW/deathdub
    echo 📖 Documentation: https://github.com/LilToreyFTW/deathdub/wiki
    echo 🌐 Live Demo: https://regenerative-addresses-tool.vercel.app
) else (
    echo.
    echo ERROR: Build failed!
    echo Please check error messages above.
    echo Make sure all required files are present:
    echo - regenerative-addresses-pro.py
    echo - Python 3.10+ with tkinter
    echo - All dependencies installed
    echo.
    echo Troubleshooting:
    echo 1. Check Python version: python --version
    echo 2. Install tkinter: python -m pip install --upgrade pip
    echo 3. Verify all files exist in current directory
)

REM Cleanup temporary files
if exist "version_info.txt" del "version_info.txt"
if exist "icon.ico" del "icon.ico"
if exist "regenerative-addresses-pro.spec" del "regenerative-addresses-pro.spec"

echo.
echo Build process completed!
pause
