#based on https://github.com/MCMi460/NSO-RPC/blob/main/scripts/macos-universal2/prep-PyQt.sh

# this script is used to prepare PyQt6 for compilation

# Download PyQt6 wheels and unpack them
python3 -m pip download --only-binary=:all: --platform=macosx_13_0_x86_64 PyQt6_Qt6
python3 -m pip download --only-binary=:all: --platform=macosx_13_0_arm64 PyQt6_Qt6
# now do the same for PyQt6-WebEngine
python3 -m pip download --only-binary=:all: --platform=macosx_13_0_x86_64 PyQt6_WebEngine
python3 -m pip download --only-binary=:all: --platform=macosx_13_0_arm64 PyQt6_WebEngine
python3 -m wheel unpack PyQt6_*arm64*.whl -d arm64
python3 -m wheel unpack PyQt6_*x86_64*.whl -d x86_64
python3 -m wheel tags --platform-tag macosx_10_14_universal2 PyQt6_*x86_64.whl


