# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../backend/gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../frontend', 'frontend'),
        ('../backend/database', 'database'),
        ('../frontend/static', 'frontend/static'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'flaskwebgui',
        'sqlalchemy',
        'flask_sqlalchemy',
        'sqlalchemy.orm',
        'sqlalchemy.ext.declarative',
        'sqlalchemy.sql.default_comparator',
        'werkzeug',
        'jinja2'
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AgeCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True to see any errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['./icon.ico']
)
