# some things modified based on https://github.com/MCMi460/NSO-RPC/blob/main/scripts/build.bat
@echo off
cd ..
@echo off


REM Install requirements
python -m pip install -r ./requirements.txt pypiwin32 winshell pyinstaller>=5.12 pyinstaller-hooks-contrib==2023.4 pillow 

REM Build the executable using PyInstaller
python -m PyInstaller --onefile --clean --noconsole --noupx --add-data "resources/*.png;resources/" --icon=eyes.icns --name="Toontown Rewritten Custom Launcher" main.py

