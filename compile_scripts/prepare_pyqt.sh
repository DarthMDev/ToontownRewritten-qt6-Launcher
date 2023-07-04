#based on https://github.com/MCMi460/NSO-RPC/blob/main/scripts/macos-universal2/prep-PyQt.sh

# this script is used to prepare PyQt6 for compilation

# Download PyQt6 wheels and unpack them
python3 -m pip download --only-binary=:all: --platform=macosx_13_0 PyQt6_Qt6
python3 -m pip download --only-binary=:all: --platform=macosx_13_0_arm64 PyQt6_Qt6
python3 -m wheel unpack PyQt6_*arm64*.whl -d PyQt6_arm64
python3 -m wheel unpack PyQt6_*x86_64*.whl -d PyQt6_x86_64

python3 -m wheel tags --platform-tag macosx_10_14_universal2 PyQt6_*x86_64.whl
python3 -m wheel unpack PyQt6_*universal2.whl --dest universal
# https://stackoverflow.com/a/46020381
merge_frameworks() {
  # $1 is the path to the binary
  binary_path="${1##universal/}"
  # lipo together the x86_64 and arm64 versions of the binary
  lipo -create -arch x86_64 "x86_64/$binary_path" "arm64/$binary_path" -output "universal/$binary_path"
}
export -f merge_frameworks

# Iterate through all the binaries in the universal wheel and merge them
find universal -perm +111 -type f -exec sh -c 'merge_frameworks "$1"' _ {} \;
python3 -m wheel pack universal/PyQt6_*

# Finally, install our universal wheel
python3 -m pip install PyQt6_*universal2.whl --force-reinstall