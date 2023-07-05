#based on https://github.com/MCMi460/NSO-RPC/blob/main/scripts/macos-universal2/prep-PyQt.sh

# this script is used to prepare PyQt6 for compilation
# it downloads the x86_64 and arm64 wheels for pyqt6 and unpacks them into separate folders
# it then uses lipo to combine them into universal2 to create a universal2 wheel

# remove any existing wheels in the directory
rm *.whl
# Download PyQt6 wheels and unpack them
python3 -m pip download --only-binary=:all: --platform=macosx_11_0_x86_64 PyQt6_Qt6
python3 -m pip download --only-binary=:all: --platform=macosx_11_0_arm64 PyQt6_Qt6
# unpack the arm64 wheel into arm64 folder
python3 -m wheel unpack PyQt6_*arm64.whl --dest pyqt6_arm64
# unpack the x86_64 wheel into x86_64 folder
python3 -m wheel unpack PyQt6_*x86_64.whl --dest pyqt6_x86_64
python3 -m wheel tags --platform-tag macosx_10_14_universal2 PyQt6_*x86_64.whl
# now do the same for PyQt6-WebEngine
python3 -m wheel unpack PyQt6_*universal2.whl --dest universal
# delete the other wheels now
rm *.whl

python3 -m pip download --only-binary=:all: --platform=macosx_11_0_x86_64 PyQt6_WebEngine
python3 -m pip download --only-binary=:all: --platform=macosx_11_0_arm64 PyQt6_WebEngine
python3 -m wheel unpack PyQt6_WebEngine*arm64.whl --dest pyqt6_arm64_webengine
python3 -m wheel unpack PyQt6_WebEngine*x86_64.whl --dest pyqt6_x86_64_webengine
python3 -m wheel tags --platform-tag macosx_10_14_universal2 PyQt6_WebEngine*x86_64.whl
# unpack the one with a none extension and universal extension
python3 -m wheel unpack PyQt6_WebEngine*none*universal2.whl --dest universal_webengine
rm *.whl


# https://stackoverflow.com/a/46020381
merge_frameworks() {
  # $1 is the path to the binary
  binary_path="${1##universal/}"
  # lipo together the x86_64 and arm64 versions of the binary
  lipo -create -arch x86_64 "pyqt6_x86_64/$binary_path" "pyqt6_arm64/$binary_path" -output "universal/$binary_path"
}
merge_frameworks_webengine()
{
  binary_path="${1##universal_webengine/}"
  lipo -create -arch x86_64 "pyqt6_x86_64_webengine/$binary_path" "pyqt6_arm64_webengine/$binary_path" -output "universal_webengine/$binary_path"
}

export -f merge_frameworks
export -f merge_frameworks_webengine
# Iterate through all the binaries in the universal wheel and merge them
find universal -perm +111 -type f -exec sh -c 'merge_frameworks "$1"' _ {} \;
find universal_webengine -perm +111 -type f -exec sh -c 'merge_frameworks_webengine "$1"' _ {} \;


# copy  universal_webengine's qt6 which contains directories  to universal's qt6  folder and merge them
cp -r universal_webengine/PyQt6_WebEngine_*/PyQt6/Qt6/* universal/PyQt6_*/PyQt6/Qt6/

# delete the universal_webengine folder
rm -rf universal_webengine
python3 -m wheel pack universal/PyQt6_*
# cleanup everything except the universal folder
rm -rf pyqt6_*
rm *.whl

