# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['ytmpcli/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['ytmpcli.cli', 'ytmpcli.downloader'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='ytmpcli',
    debug=False,
    console=True,
    icon=None,
)
