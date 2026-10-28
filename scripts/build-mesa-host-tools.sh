#!/usr/bin/env bash
set -euo pipefail

if [[ $# != 1 ]]; then
    echo "Usage: $0 ANDROID_SOURCE_ROOT" >&2
    exit 2
fi
source_root=$(cd "$1" && pwd)
build_dir="$source_root/out/mesa-spark-host"
destination="$source_root/mesa-host-tools/bin"

# Requires a native x86_64 Mesa build environment with LLVM/Clang development
# libraries, libclc, Rust, bindgen, cbindgen, Python Mako/PyYAML, Meson and Ninja.
# Keep AOSP's cross-compiling rustc wrapper out of this native tool build.
meson setup "$build_dir" "$source_root/external/mesa" \
    -Dbuildtype=release -Dbuild-tests=false \
    -Dplatforms=[] -Dgallium-drivers=asahi,panfrost -Dvulkan-drivers=imagination \
    -Dllvm=enabled -Dmesa-clc=enabled -Dprecomp-compiler=enabled \
    -Dinstall-mesa-clc=true -Dinstall-precomp-compiler=true \
    -Dglx=disabled -Degl=disabled -Dgbm=disabled \
    -Dgles1=disabled -Dgles2=disabled -Dopengl=false
targets=(src/compiler/spirv/vtn_bindgen2 src/asahi/clc/asahi_clc \
         src/panfrost/clc/panfrost_compile src/imagination/pco/uscgen/pco_clc)
ninja -C "$build_dir" "${targets[@]}"
mkdir -p "$destination"
for target in "${targets[@]}"; do
    install -m755 "$build_dir/$target" "$destination/${target##*/}"
done
