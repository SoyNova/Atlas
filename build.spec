
block_cipher = None

# ============= CONFIGURACIÓN PRINCIPAL =============
a = Analysis(
    ['script.py'],  # Archivo principal
    pathex=[],  # Ruta de búsqueda adicional
    binaries=[],  # Binarios externos
    datas=[('web', 'web')],  # Carpeta web de Eel
    hiddenimports=[],  # Imports ocultos
    hookspath=[],  # Ruta de hooks
    hooksconfig={},  # Config hooks
    runtime_hooks=[],  # Runtime hooks
    excludes=[],  # Módulos a excluir
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,  # Ofuscación
    noarchive=False  # True para modo depuración
)

# ============= PAQUETE .PYZ =============
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher  # Ofuscación del bytecode
)

# ============= EJECUTABLE FINAL =============
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Atlas',  # Nombre del .exe
    debug=False,  # No generar información de debug
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Comprimir con UPX (recomendado)
    console=False,  # Ocultar consola (--noconsole)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Icono personalizado (opcional)
)

