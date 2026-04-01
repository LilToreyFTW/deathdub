#!/usr/bin/env python3
"""
Test script to verify requests module works in PyInstaller build
"""

import sys
import os

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Python path:", sys.path[:3])
print("Current directory:", os.getcwd())

try:
    import requests
    print("✅ requests module imported successfully")
    print("requests version:", requests.__version__)
    
    # Test a simple request
    try:
        response = requests.get('https://httpbin.org/get', timeout=5)
        print("✅ requests.get() works - Status:", response.status_code)
    except Exception as e:
        print("❌ requests.get() failed:", str(e))
        
except ImportError as e:
    print("❌ Failed to import requests:", str(e))
    print("Available modules:")
    import pkgutil
    for _, name, _ in pkgutil.iter_modules():
        if 'request' in name.lower():
            print(f"  - {name}")

print("\nChecking urllib availability...")
try:
    import urllib.request
    print("✅ urllib.request available")
except ImportError as e:
    print("❌ urllib.request not available:", str(e))

print("\nChecking certifi availability...")
try:
    import certifi
    print("✅ certifi available, version:", certifi.__version__)
except ImportError as e:
    print("❌ certifi not available:", str(e))

print("\nChecking urllib3 availability...")
try:
    import urllib3
    print("✅ urllib3 available, version:", urllib3.__version__)
except ImportError as e:
    print("❌ urllib3 not available:", str(e))

input("\nPress Enter to exit...")
