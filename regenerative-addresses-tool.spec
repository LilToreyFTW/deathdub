# -*- mode: python ; coding: utf-8 -*-

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
        'requests.adapters',
        'requests.auth',
        'requests.exceptions',
        'requests.sessions',
        'requests.utils',
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
        'cryptography',
        'urllib',
        'urllib.request',
        'urllib.parse',
        'urllib.error',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Collect all requests dependencies
a.datas += Tree([(p, p) for p in a.binaries if 'requests' in p[0].lower()])
a.datas += Tree([(p, p) for p in a.binaries if 'urllib3' in p[0].lower()])
a.datas += Tree([(p, p) for p in a.binaries if 'certifi' in p[0].lower()])
a.datas += Tree([(p, p) for p in a.binaries if 'charset' in p[0].lower()])
a.datas += Tree([(p, p) for p in a.binaries if 'idna' in p[0].lower()])

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
    icon='icon.ico',
    version='version_info.txt',
)
