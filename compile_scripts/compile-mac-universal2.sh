export PYTHON_VERSION
# give the only the first 2 numbers  (major and minor)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
python3 -m pip install --upgrade pip
python3 -m pip install wheel
wget https://files.pythonhosted.org/packages/d5/5d/0342b29e4cb20a227642d28f193dc752e8d17694ffd8e23e662f72ae84e6/bsdiff4-1.2.3-cp311-cp311-macosx_10_9_universal2.whl
python3 -m pip install bsdiff4-1.2.3-cp311-cp311-macosx_10_9_universal2.whl
python3 -m pip install -r ../requirements.txt py2app
./prepare_pyqt.sh
cd ..
py2applet --make-setup main.py
sed -i '' -e "s/)/    name='Toontown Rewritten Custom Launcher')/" setup.py
python3 setup.py py2app -O2 --arch=universal2 --resources resources --iconfile eyes.icns
cp -r compile_scripts/universal/PyQt6_*/PyQt6/Qt6/* "./dist/Toontown Rewritten Custom Launcher.app/Contents/Resources/lib/python$PYTHON_VERSION/PyQt6/Qt6/"
# next we cleanup any qt files that are not needed
python3 compile_scripts/cleanup.py
codesign --force --deep --sign - dist/Toontown\ Rewritten\ Custom\ Launcher.app/Contents/MacOS/*
open dist

