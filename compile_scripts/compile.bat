@echo off
cd ..
pyinstaller --onefile main.py --clean --noconsole --add-data "resources/*.png;resources/" -n "Toontown Rewritten Custom Launcher.exe" -i "eyes.icns"
rmdir build /s /q

