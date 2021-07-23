# -*- mode: python ; coding: utf-8 -*-
import os
import glob

block_cipher = None

# current_path = os.path.abspath(__file__)
current_path = os.path.abspath(".\\pack\\transUnit.spec")
print(current_path)
for i in range(2):
    pathex = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    current_path = pathex
pathex = pathex + "\\"

a = Analysis([pathex + 'transUnit_login.py'],
             pathex=[pathex],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

def extra_datas(mydir):
    def rec_glob(p, files):
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas

# append the 'config' dir
a.datas += extra_datas('lib')
a.datas += extra_datas('resource')
a.datas += extra_datas('cache')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='DHMS传输单元服务部署工具',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , uac_admin=True, icon=pathex+'resource\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='DHMS传输单元服务部署工具')
