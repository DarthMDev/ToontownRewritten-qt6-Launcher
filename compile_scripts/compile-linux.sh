


sudo apt-get install -y python3-pip
# install qt6
sudo apt-get install build-essential libgl1-mesa-dev

sudo apt-get install -y python3-pyqt6
cd ..

# install requirements 
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller>=5.12 pyinstaller-hooks-contrib==2023.4 pillow
pyinstaller  --onefile --clean --noconsole --noupx --add-data "resources/*.png:resources/" --icon=eyes.icns --name="Toontown Rewritten Custom Launcher" main.py


