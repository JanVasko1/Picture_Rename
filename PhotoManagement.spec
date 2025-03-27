# -*- mode: python ; coding: utf-8 -*-

# Define fixed output folders
DISTPATH='D:\_Helper\Application\Pyinstaller\PhotoManagement'
WORKPATH='D:\_Helper\Application\Pyinstaller\PhotoManagement'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-Picture_Rename\\Lib\\site-packages\\iconipy\\assets', 'iconipy\\assets'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-Picture_Rename\\Lib\\site-packages\\piexif', 'piexif'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-Picture_Rename\\Lib\\site-packages\\lat_lon_parser', 'lat_lon_parser'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-Picture_Rename\\Lib\\site-packages\\windows_metadata', 'windows_metadata'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-Picture_Rename\\Lib\\site-packages\\subprocess', 'subprocess'),
        ('C:\\Users\\CZ011845\\AppData\\Local\\miniconda3\\envs\\ENV-Picture_Rename\\Lib\\site-packages\\CTkColorPicker', 'CTkColorPicker')],
    hiddenimports=['iconipy', 'CTkColorPicker', 'subprocess', 'piexif', 'lat_lon_parser', 'subprocess', 'windows_metadata'],
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
    [],
    exclude_binaries=True,
    name='PhotoManagement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Libs\\GUI\\Icons\\Logo.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PhotoManage',
)
