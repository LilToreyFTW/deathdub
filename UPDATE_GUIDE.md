# Auto-Update System Guide

## 🔄 **Auto-Update Features**

Your regenerative-addresses tool now includes automatic updating from your GitHub repository: `https://github.com/LilToreyFTW/deathdub`

## 🚀 **How It Works**

### **Automatic Updates:**
- **Background checking** every hour
- **GitHub API** integration for release detection
- **Version comparison** with semantic versioning
- **User confirmation** before installing updates

### **Manual Updates:**
- **"Check Updates"** button in the main interface
- **Download progress** indicator
- **Automatic backup** before update
- **Rollback** if update fails

## 📋 **Update Process**

### **1. Detection**
- Checks GitHub releases API
- Compares `tag_name` with current version
- Skips versions user has declined

### **2. Download**
- Downloads release ZIP from GitHub
- Shows progress bar
- Verifies download integrity

### **3. Installation**
- Creates backup of current files
- Extracts new version
- Replaces updated files
- Restores backup on failure

### **4. Restart**
- Auto-restarts application
- Loads new version
- Shows success message

## 🔧 **Configuration**

### **Current Settings:**
```python
# In auto_updater.py
current_version = "1.0.0"
repo_url = "https://github.com/LilToreyFTW/deathdub"
update_interval = 3600  # 1 hour
```

### **To Update Settings:**
1. Edit `auto_updater.py`
2. Change `current_version` when you release updates
3. Modify `update_interval` for check frequency

## 📦 **Release Process**

### **When You Update Your Tool:**

1. **Update version** in `auto_updater.py`:
   ```python
   current_version = "1.1.0"  # Example
   ```

2. **Commit changes** to your GitHub repo:
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   git push
   ```

3. **Create GitHub Release**:
   - Go to your repo on GitHub
   - Click "Releases" → "Create a new release"
   - Tag: `v1.1.0`
   - Title: "Version 1.1.0"
   - Description: Add release notes
   - Publish release

### **What Gets Updated:**
- `regenerative-addresses.py` - Main application
- `kali_credential_obtainer.py` - Kali tools module
- `users.json` - User database (preserved if exists)
- `all_proxies.txt` - Proxy lists (preserved if exists)

## 🛡️ **Security Features**

### **Update Safety:**
- **Backup creation** before any changes
- **Rollback** on installation failure
- **User confirmation** required
- **Version skipping** option
- **Integrity verification** during download

### **Protected Files:**
- User credentials (`users.json`)
- Custom proxy lists
- Generated logs and credentials

## 🎯 **User Experience**

### **Update Dialog:**
- Shows current vs latest version
- Displays release notes
- Download progress bar
- Install/Cancel/Skip options

### **Background Updates:**
- Silent checking every hour
- Non-blocking operation
- Status bar notifications
- No interruption to workflow

## 🔍 **Troubleshooting**

### **Common Issues:**
- **Network connectivity** - Check internet connection
- **GitHub API limits** - Updates may be delayed
- **File permissions** - Ensure write access
- **Antivirus blocking** - Add to exceptions

### **Manual Recovery:**
If auto-update fails:
1. Restore from `backup/` folder
2. Download release manually from GitHub
3. Extract and replace files manually

## 📊 **Update Log**

### **Version History:**
- `v1.0.0` - Initial release with auto-updater
- Future versions will be listed here automatically

### **Update Statistics:**
- Check frequency: Every hour
- Backup location: `./backup/`
- Temp location: `./temp_update/`
- Skip file: `skip_version.txt`

## 🚀 **Ready to Use**

The auto-updater is now integrated and will:
- ✅ Check your GitHub repo for updates
- ✅ Download and install new versions
- ✅ Backup current installation
- ✅ Handle updates automatically

**Just push releases to your GitHub repo and users will get notified automatically!**
