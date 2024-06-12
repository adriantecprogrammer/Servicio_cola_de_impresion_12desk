# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\agera\\PycharmProjects\\Servicio_cola_de_impresion_12desk\\Servicio_cola_de_impresion_12desk\\interfaz.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\agera\\PycharmProjects\\Servicio_cola_de_impresion_12desk\\Servicio_cola_de_impresion_12desk\\.env', '.'),
           ('C:/Users/agera/AppData/Local/Programs/Python/Python312/Lib/site-packages/mysql/connector/locales', 'mysql/connector/locales'),
           ],
    hiddenimports=['mysql.connector'],
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
    name='interfaz',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='interfaz',
)
