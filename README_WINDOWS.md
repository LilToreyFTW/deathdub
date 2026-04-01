# Windows Executable Build Instructions

## 🪟 **Easy Windows .exe Build**

### **Option 1: Quick Build (Recommended)**
1. Copy these files to a Windows machine:
   - `regenerative-addresses.py`
   - `kali_credential_obtainer.py`
   - `all_proxies.txt`
   - `users.json`

2. Run the provided batch file:
   ```
   WINDOWS_BUILD_SCRIPT.bat
   ```

3. Your Windows .exe will be created in `dist\RegenerativeAddresses.exe`

### **Option 2: Manual Build**
On Windows machine with Python 3.9+:

```cmd
# Install PyInstaller
python -m pip install pyinstaller

# Build executable
python -m PyInstaller --onefile --windowed --name "RegenerativeAddresses" regenerative-addresses.py
```

## 📦 **Package Contents Needed**

Copy these files to Windows before building:

### **Core Files:**
- ✅ `regenerative-addresses.py` - Main application
- ✅ `kali_credential_obtainer.py` - Kali tools module
- ✅ `users.json` - User database (admin:admin)

### **Proxy Files:**
- ✅ `all_proxies.txt` - Master proxy list (18,835+ addresses)
- ✅ `proxies.txt` - Additional proxies
- ✅ `http_proxies2.txt` - HTTP proxies
- ✅ `socks4_proxies2.txt` - SOCKS4 proxies
- ✅ `socks5_proxies2.txt` - SOCKS5 proxies

## 🚀 **After Building Windows .exe**

### **Single File Distribution:**
The built `RegenerativeAddresses.exe` includes everything - no additional files needed!

### **Login Credentials:**
- Username: `admin`
- Password: `admin`

### **Features Included:**
- 🔐 User authentication system
- 🔗 Link regeneration (7 techniques)
- 🛡️ Kali Linux tools integration
- 📤 Force re-login capabilities
- 🌊 18,835+ proxy addresses
- 📊 System info capture

## 📋 **System Requirements**

### **Windows:**
- Windows 7/8/10/11 (64-bit)
- No Python installation needed (standalone .exe)
- No additional dependencies

### **Size:**
- Expected .exe size: ~15-20 MB
- Single file - portable and self-contained

## 🎯 **Usage on Windows**

1. **Double-click** `RegenerativeAddresses.exe`
2. **Login** with admin/admin
3. **Select "Link Regenerator"**
4. **Paste URL** and click regenerate
5. **View credentials** in yellow box
6. **Force re-login** with button

## 🔧 **Troubleshooting**

### **Common Issues:**
- **Antivirus blocks**: Add to exceptions
- **Windows Defender**: Allow the application
- **Permission denied**: Run as Administrator
- **Missing dependencies**: Rebuild with all files present

### **Build Errors:**
- Ensure Python 3.9+ is installed
- Check all files are in same directory
- Run Command Prompt as Administrator

## 📧 **Support**

The Windows .exe will work identically to the Linux version with all features:
- Link regeneration
- Credential generation
- Kali tools integration (simulated on Windows)
- Proxy management
- User authentication

**Ready to build on Windows!**
