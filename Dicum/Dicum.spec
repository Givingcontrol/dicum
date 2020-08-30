# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

resources = [
        ("resources/fonts", "fonts"),
        ("resources/icons", "icons"),
        ("resources/images/README","images"),
        ("resources/images/bg.png","images"),
        ("resources/js", "js"),
        ("resources/templates", "templates")]

a = Analysis(['Dicum.py'],
             pathex=['/home/jonas/Projects/dicum/Dicum'],
             binaries=[],
             datas=resources,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Dicum',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
