# run this session in rosetta 2
arch -x86_64 zsh
python3 -m pip install --upgrade pip
python3 -m pip install wheel
python3 -m pip install -r ../requirements.txt py2app
cd ..
py2applet --make-setup main.py
sed -i '' -e "s/)/    name='Toontown Rewritten Custom Launcher')/" setup.py
python3 setup.py py2app -O2 --arch=x86_64 --resources resources --iconfile eyes.icns
# next we cleanup any qt files that are not needed
python3 compile_scripts/cleanup.py
codesign --force --deep --sign - dist/Toontown\ Rewritten\ Custom\ Launcher.app/Contents/MacOS/*
open dist

