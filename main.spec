# -*- mode: python ; coding: utf-8 -*-

# To build, run "pyinstaller main.spec --noconfirm"

block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\\taku-n\\scadama'],
             binaries=[],
             datas=[],
             hiddenimports=['MetaTrader5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('impl.py', '.\\impl.py', 'DATA')]
a.datas += [('widget.py', '.\\widget.py', 'DATA')]
a.datas += [('config.toml', '.\\config.toml', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
