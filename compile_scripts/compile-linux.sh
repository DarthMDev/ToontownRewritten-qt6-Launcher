


sudo apt-get install -y python3-pip
# install qt6
sudo apt-get install build-essential libgl1-mesa-dev

sudo apt-get install -y qt6-base-dev
sudo apt-get install -y python3-pyqt6
cd ..
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller pillow
pyinstaller --onefile --clean --add-data "resources/*.png:resources/"  main.py --name "Toontown Rewritten Custom Launcher" -i "eyes.icns"


