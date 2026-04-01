# Link Regeneration Guide

## Overview

The Regenerative Addresses Tool now includes a powerful **Link Regenerator** feature that transforms any URL into multiple variations using various techniques.

## 🔐 **User Authentication System**

### Features:
- **Login System**: Secure user authentication with SHA-256 password hashing
- **Registration**: New user account creation
- **Session Management**: 5-minute session timeout with automatic re-login
- **User Storage**: Local user database in `users.json`

### How to Use:
1. **Register**: Create a new account with username and password
2. **Login**: Enter credentials to access the tool
3. **Session**: Automatically logged out after 5 minutes of inactivity
4. **Logout**: Manual logout option available

## 🔗 **Link Regeneration Features**

### Available Techniques:
1. **Parameter Addition**: Adds UTM, tracking, or custom parameters
2. **Subdomain Change**: Modifies or adds subdomains (www, m, app, etc.)
3. **Path Segments**: Adds directory-like paths (/go, /redirect, etc.)
4. **TLD Change**: Switches top-level domains (.com → .net, .org, etc.)
5. **Tracking Parameters**: Adds Facebook/Google tracking IDs
6. **URL Shortening**: Creates bit.ly-style short links
7. **Affiliate Parameters**: Adds affiliate/referral codes

### Example Transformations:

**Original**: `https://example.com/product`

**Regenerated Examples**:
- `https://example.com/product?utm_source=facebook&session_id=a1b2c3d4`
- `https://m.example.com/product/go`
- `https://example.org/product?fbclid=xyz123abc456`
- `https://bit.ly/3KjLmN9`
- `https://shop.example.com/product?aff=123456`

## 🛠️ **How to Use Link Regenerator**

1. **Login** to the application
2. Select **"Link Regenerator"** from the dropdown
3. **Paste your link** in the text area
4. Click **"Regenerate Link"** or **"Generate Address"**
5. Set **quantity** (1-100 variations)
6. Choose **output format** (Plain, JSON, CSV, Hex)
7. **Copy** results to clipboard

## 🎯 **Use Cases**

### Marketing & Analytics:
- Create campaign tracking links
- Generate UTM parameter variations
- Test different affiliate codes

### Testing & Development:
- Create test URL variations
- Simulate different referral sources
- Generate mock tracking data

### Privacy & Anonymity:
- Obscure original URLs
- Create redirect chains
- Add tracking noise

## ⚙️ **Technical Details**

### Regeneration Algorithm:
- Applies 1-3 random techniques per URL
- Each technique has multiple variations
- Maintains URL structure while adding modifications
- Supports HTTP, HTTPS, and various domain formats

### Session Management:
- 5-minute inactivity timeout
- Automatic session monitoring
- Secure password storage
- Local user authentication

### Output Formats:
- **Plain**: Simple text list
- **JSON**: Structured data format
- **CSV**: Spreadsheet-compatible
- **Hex**: Hexadecimal encoding

## 🔒 **Security Features**

- Password hashing with SHA-256
- Session timeout protection
- Local user data storage
- No external authentication dependencies

## 📝 **Tips for Best Results**

1. **Start with clean URLs** - Remove existing parameters for best regeneration
2. **Use HTTPS** - More secure and professional
3. **Test variations** - Not all regenerated URLs may work
4. **Batch generation** - Create multiple variations at once
5. **Combine with proxies** - Use generated proxies with regenerated links

## 🚀 **Advanced Usage**

### Custom Parameters:
The tool automatically adds realistic parameters like:
- `utm_source`, `utm_medium`, `utm_campaign`
- `fbclid`, `gclid`, `msclkid`
- `aff`, `partner`, `ref`, `promo`

### Domain Variations:
- Subdomain changes (www → m → app)
- TLD switching (.com → .net → .org)
- Short URL generation

### Path Modifications:
- Marketing paths (/go, /redirect)
- Action paths (/click, /visit)
- Tracking paths (/view, /open)

---

**Note**: This tool is for testing and development purposes. Use responsibly and ensure compliance with applicable laws and terms of service.
