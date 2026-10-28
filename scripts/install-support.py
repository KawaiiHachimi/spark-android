#!/usr/bin/env python3
"""Install relocatable source helpers for the captured Android Mesa build."""
import argparse
import os
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path, help='Android source root')
args = parser.parse_args()
root = args.source.resolve()
if not (root / 'build/envsetup.sh').is_file():
    parser.error('not an Android source root')
destination = root / 'nvk-rust-bin'
destination.mkdir(exist_ok=True)
for name in ['rustc', 'extract-gb20b-610.py']:
    target = destination / name
    text = (PACKAGE / 'support/nvk-rust-bin' / name).read_text()
    # Relocate the original wrapper's only absolute source-root path.
    text = text.replace('/home/cool/lineage24/', str(root) + '/')
    if target.exists() and target.read_text() != text:
        raise SystemExit(f'Refusing to overwrite a different helper: {target}')
    target.write_text(text)
    target.chmod(0o755)
print(destination)

# Reproduce two observed local linker-search symlinks using relative targets.
# The library is produced by the Android build; a dangling link is expected
# before lib c++ has been built.
library = root / 'out/target/product/Generic_arm64/obj/SHARED_LIBRARIES/libc++.vendor_intermediates/libc++.vendor.so'
runtime = root / 'prebuilts/clang/host/linux-x86/clang-r596125/lib/clang/22/lib/linux'
for directory in [runtime, runtime / 'aarch64']:
    if not directory.is_dir():
        raise SystemExit(f'Captured Clang runtime directory is missing: {directory}')
    link = directory / 'libc++.so'
    if link.is_symlink() and link.resolve() == library:
        continue
    if link.exists() or link.is_symlink():
        raise SystemExit(f'Refusing to overwrite an existing runtime file: {link}')
    link.symlink_to(os.path.relpath(library, directory))
    print(link)
