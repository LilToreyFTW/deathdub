# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['regenerative-addresses-new.py'],
    pathex=[],
    binaries=[],
    datas=[('all_proxies.txt', '.'), ('proxies.txt', '.'), ('users.json', '.'), ('kali_credential_obtainer.py', '.'), ('auto_updater.py', '.'), ('proxy_manager.py', '.'), ('src', 'src'), ('index.php', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RegenerativeAddresses_v2',
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
)
