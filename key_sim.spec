# -*- mode: python -*-
import shutil
import os
import site

source_path = os.path.abspath('')
python_packages_path = site.getsitepackages()[0]
data_static_path = os.path.abspath('static/')
data_templates_path = os.path.abspath('templates/')
data_icon_path = os.path.abspath('static/images/system_icons/favicon.ico')
data_key_event_list_path = os.path.abspath('key_events.json')
app_name="keysim_gui"

matches = ["LICENSE.txt","METADATA","PKG-INFO"]
lics = []
print("Find 3rd party dependency license files")
for root, dir, files in os.walk(python_packages_path):
    for file in files:
            if file in matches:
               src = os.path.join(root, file)
               dest = os.path.join(DISTPATH, app_name, "python_package_licenses", os.path.basename(root))
               lics.append((src, dest))
               print("\tLicense file:", os.path.join(root, file))

block_cipher = None
a = Analysis(['key_sim.py'],
             pathex=[source_path],
             binaries=[],
             datas  = [(data_static_path,'static'), (data_templates_path,'templates')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=app_name,
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=data_icon_path)

coll = COLLECT(exe,
	           a.binaries,
               a.zipfiles,
               a.datas,
               name=app_name,
               strip=False,
               upx=True)

shutil.copytree(data_static_path, os.path.join(DISTPATH,app_name,"static"), dirs_exist_ok=True)
shutil.copy(data_key_event_list_path, os.path.join(DISTPATH, app_name, "key_events.json"))
for file in lics:
    os.makedirs(os.path.dirname(file[1]), exist_ok=True)
    shutil.copy(file[0], file[1])
