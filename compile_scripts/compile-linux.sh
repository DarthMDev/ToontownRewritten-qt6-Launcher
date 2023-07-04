


sudo apt-get install -y python3-pip
# install qt6
sudo apt-get install build-essential libgl1-mesa-dev

sudo apt-get install -y qt6-base-dev
sudo apt-get install -y python3-pyqt6
cd ..
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt pyinstaller
rm -rf bin
pyinstaller --onefile main.py
rm -rf build
mv dist bin
cp -r resources bin/resources
sleep 1 

