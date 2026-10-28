# Source inventory

Captured 2026-10-28 from the existing checkout; upstream refs were not advanced.

| Repository | Clean base | Captured result | Patches |
|---|---|---|---|
| `build/make` | `e7cc87a995b25ae412aefa493d2b9c2b0157f29d` | `8577ba6c9427a5cd2951c83ffd54f658321bea5c` | 1 |
| `build/soong` | `5ea236479501d50a4a0eafb568f4f35d1bdda3cb` | `b76f99bbed601a0d73621a7e30c214eca1c87590` | 1 |
| `device/mainline/common` | `5f372f1bd3c439275c64e6a4f0c16639e8da58d0` | unchanged | 0 |
| `device/mainline/generic` | `4e5103bb1c51410d3d0c5305758cd51124276be1` | `f98c3f0de1526e5c4c61a2184d8c09e43fa0d440` | 2 |
| `external/alsa-lib` | `533b21f75eb2bd3fe46e9259dccf1628e318f859` | unchanged | 0 |
| `external/alsa-ucm-conf` | `b695e87520201d31a9207a1108648c3f83f71e11` | unchanged | 0 |
| `external/debian-linux` | `9f34e3aa86f30b352343b4f2c737617763da8199` | unchanged | 0 |
| `external/drm_hwcomposer-upstream` | `30e7b376bbccc4977a17e38ee881aa08580a6a7a` | unchanged | 0 |
| `external/libdisplay-info-upstream` | `dffa9dee319f956c94a2cb4a853f9d55ff84a560` | unchanged | 0 |
| `external/linux-firmware-mainline` | `ef88d24dfc10e30826789b82fca417d6f913ee2a` | unchanged | 0 |
| `external/mesa` | `5a6bb76986d2d111599baf18e1dcd20b5ffd02c4` | `773763de5bd2d5b1e77b451bb85b1cf3e6d3ff16` | 4 |
| `external/minigbm-upstream` | `0111c9e1033106dc85899eea1076e4579200d75b` | unchanged | 0 |
| `external/tinyhal` | `e2e5a2ecdeb20b99d5f5ad4a3472c96c45faeaa5` | unchanged | 0 |
| `external/zstd` | `1bfdf8aef6bdec0e817c1f75aeaf382db22de668` | `ab3b52aa32c1f1d4afc916a1e886ef4b015dfb14` | 1 |
| `frameworks/native` | `0ec1966edafb792ffefa81879b24364528f823aa` | `cccd2c87fbe1aa936be8680aa11ddae37b06c208` | 1 |
| `hardware/mainline/common` | `5a4c000ed850733f609b00fcc9c39c118c8cce84` | unchanged | 0 |
| `kernel/mainline/android-mainline` | `c4617c26c0908a8867a2d57e59023f1c2f435a10` | `9d73fe9964f7017ea5c9e3696f21caaad5d87c0b` | 4 |
| `kernel/mainline/configs` | `dc05b10df0b9efee05dc68f0d8166d4f2713e48f` | unchanged | 0 |
| `prebuilts/bootmgr` | `811ba971e891b1f3e7412dfcaac633af5517892f` | unchanged | 0 |
| `prebuilts/mesa-build-dep` | `1121f16432d25f08db3844588f12e1e2eaf8f42d` | unchanged | 0 |
| `system/core` | `1375cc767964bbac2070bc41ebc3c864589846b4` | `59c4402fe613886f954790d5e62c65ad206582b4` | 1 |
| `system/memory/libmeminfo` | `d59c960b1fb93377bf68664918031ea5fe709f89` | `499de099ed9f3dda6aa20a67c9a1f526ba6b7aff` | 1 |
| `vendor/mainline` | `aece1ef90901246089683732f75bd04453b7fe51` | unchanged | 0 |

## Captured commits

### build/make

1 file changed, 1 insertion(+), 2 deletions(-)

- `8577ba6c9427a5cd2951c83ffd54f658321bea5c` build: use SerialGC and a larger Java code cache

### build/soong

2 files changed, 10 insertions(+), 4 deletions(-)

- `b76f99bbed601a0d73621a7e30c214eca1c87590` java: tune compiler JVMs for the Spark image build

### device/mainline/generic

9 files changed, 84 insertions(+), 35 deletions(-)

- `34788c42dac5d096b8dc7016d20223b4fde5bf54` generic: refresh mainline prerequisite patch documentation
- `f98c3f0de1526e5c4c61a2184d8c09e43fa0d440` generic: integrate DGX Spark graphics and arm64 live ISO

### external/mesa

7071 files changed, 1034008 insertions(+), 550678 deletions(-)

- `42c8a038db50c8be172766926f66c9cf49e8e33a` mesa: import upstream 26.2.2 for Blackwell support
- `7785c133ee76415b027d18d1f41c62816ce4d300` android: integrate Mesa 26 NVK with the AOSP build tools
- `8bfe563d0f4772cf92602e9af5db7b5a5125cc56` nouveau: preserve NVK Android and nvgpu integration
- `773763de5bd2d5b1e77b451bb85b1cf3e6d3ff16` mesa: preserve local compatibility and offline wrap metadata

### external/zstd

1 file changed, 1 insertion(+)

- `ab3b52aa32c1f1d4afc916a1e886ef4b015dfb14` zstd: allow vendor subpackages to use libzstd

### frameworks/native

1 file changed, 6 insertions(+)

- `cccd2c87fbe1aa936be8680aa11ddae37b06c208` data: expose the Vulkan 1.4 feature XML as a prebuilt

### system/core

1 file changed, 1 insertion(+), 1 deletion(-)

- `59c4402fe613886f954790d5e62c65ad206582b4` ueventd: search the mounted mainline firmware image

### system/memory/libmeminfo

1 file changed, 10 insertions(+)

- `499de099ed9f3dda6aa20a67c9a1f526ba6b7aff` libmeminfo: handle kernels without the GPU memory BPF map

### kernel/mainline/android-mainline

197 files changed, 10743 insertions(+), 710 deletions(-)

- `fe616e739431169443a4f155eacf78239424fa51` selinux: honor the mainline live image permissive boot option
- `692a4092bdde11237886d6dda6c66ccbd80a38ba` drm/virtio: restore default context creation for generic guests
- `21d7df1a68e81ca814fcb7008d45e74861d4450d` kconfig: provide the empty external configuration hook
- `9d73fe9964f7017ea5c9e3696f21caaad5d87c0b` drm/nouveau: integrate GB20B, GSP 610 and coherent display support
