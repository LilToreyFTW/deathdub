# Proxy Usage Guide

## Available Proxies

Your regenerative-addresses tool now includes **7,419+ free proxy addresses** from multiple sources:

### Proxy Types Available:
- **HTTP Proxies**: 5,957 addresses
- **SOCKS4 Proxies**: 741 addresses  
- **SOCKS5 Proxies**: 721 addresses

### Sources:
1. **Proxifly Free Proxy List** - Updated every 5 minutes
2. **SpeedX Proxy List** - GitHub repository with active proxies
3. **Combined master list** - 7,419 unique proxies

## How to Use

### In the GUI Tool:
1. Select **"Proxy Address"** from the dropdown menu
2. Set the quantity (1-100 proxies at once)
3. Choose output format (Plain, JSON, CSV, or Hex)
4. Click **"Generate Address"** to get random proxies
5. Use **"Copy to Clipboard"** to export them

### Proxy Formats:
- HTTP: `http://IP:PORT`
- HTTPS: `https://IP:PORT` 
- SOCKS4: `socks4://IP:PORT`
- SOCKS5: `socks5://IP:PORT`

### Example Output:
```
http://192.111.137.37:18762
socks5://72.49.49.11:31034
http://208.102.51.6:58208
socks4://69.61.200.104:36181
```

## Updating Proxies

To refresh the proxy list with the latest addresses:

```bash
python3 proxy_manager.py
```

This will:
- Download fresh proxies from all sources
- Remove duplicates
- Update the master `all_proxies.txt` file
- Show statistics about the new proxy collection

## Important Notes

⚠️ **Free Proxy Limitations:**
- These are public proxies that may be slow or unreliable
- Not suitable for high-security applications
- Some may not work or have high latency
- Use for testing, development, or educational purposes

✅ **Best Practices:**
- Test proxies before using in production
- Rotate between different proxies
- Monitor connection timeouts
- Have backup proxies ready

## Proxy Testing

To test if proxies work, you can use tools like:
- `curl --proxy http://IP:PORT http://example.com`
- Proxy testing scripts
- Online proxy verification services

## File Locations

- `all_proxies.txt` - Master proxy list (7,419 proxies)
- `proxifly_all.txt` - Proxifly source proxies
- `speedx_http.txt` - SpeedX HTTP proxies
- `proxy_manager.py` - Proxy download/update script
