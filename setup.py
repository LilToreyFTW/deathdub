import sys
from cx_Freeze import setup, Executable

# Dependencies for rebuilt tool
build_exe_options = {
    "packages": [
        "tkinter", "tkinter.ttk", "tkinter.scrolledtext", "os", "sys", "json", 
        "hashlib", "uuid", "random", "string", "ipaddress", "re", "datetime", 
        "urllib.request", "base64", "time", "threading", "subprocess", "getpass", 
        "platform", "webbrowser", "pathlib"
    ],
    "excludes": ["matplotlib", "numpy", "scipy"],
    "include_files": [
        ("all_proxies.txt", "all_proxies.txt"),
        ("proxies.txt", "proxies.txt"),
        ("http_proxies.txt", "http_proxies.txt"),
        ("http_proxies2.txt", "http_proxies2.txt"),
        ("socks4_proxies.txt", "socks4_proxies.txt"),
        ("socks4_proxies2.txt", "socks4_proxies2.txt"),
        ("socks5_proxies.txt", "socks5_proxies.txt"),
        ("socks5_proxies2.txt", "socks5_proxies2.txt"),
        ("users.json", "users.json"),
        ("kali_credential_obtainer.py", "kali_credential_obtainer.py"),
        ("auto_updater.py", "auto_updater.py"),
        ("proxy_manager.py", "proxy_manager.py"),
        ("src", "src"),
        ("index.php", "index.php")
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Tells cx_Freeze this is a GUI application

setup(
    name="RegenerativeAddresses",
    version="2.0.0",
    description="Regenerative Addresses Tool v2.0 - Educational Security Testing",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "regenerative-addresses-new.py",
            base=base,
            target_name="RegenerativeAddresses.exe",
            icon=None,
        )
    ],
)
