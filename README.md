# spark-android

DGX Spark（GB10 / GB20B）的 LineageOS 24.0 / `Generic_arm64` 适配补丁，按源码仓库组织。基于当前源码树于 2026-10-28 整理，共 **9 个仓库、16 个补丁**。

| 源码仓库 | 补丁概述 |
|---|---|
| `kernel/mainline/android-mainline` | Nouveau GB20B、GSP/FMC 610.43.03、内存与显示 IOVA 支持；另含通用 mainline 的 SELinux、virtio 和 Kconfig 补丁。 |
| `external/mesa` | 升级至 26.2.2；NVK/NIL、Android 缓冲区及 nvgpu 后端；AOSP Rust/bindgen 构建集成与离线依赖元数据。 |
| `device/mainline/generic` | NVK + Zink、Nouveau atomic 与固件加载、vendor GBM allocator、Vulkan 特性声明、arm64 GRUB Live ISO；更新依赖补丁文档。 |
| `frameworks/native` | 增加 Vulkan 1.4 特性 XML 的 prebuilt 模块。 |
| `system/core` | ueventd 搜索 `/mnt/vendor/firmware/`。 |
| `system/memory/libmeminfo` | 兼容没有 GPU 内存 BPF map 的内核。 |
| `external/zstd` | 放开 vendor 子包的库可见性。 |
| `build/make`、`build/soong` | 保留构建当前镜像使用的 Java/Kotlin GC、代码缓存及编译层级调整。 |

每个仓库的补丁目录位于 `patches/<源码路径>/`，`series` 记录顺序。Mesa 升级补丁较大，使用 `.patch.xz` 存储，应用脚本自动解压。

## 应用

在空目录同步精确的干净基线（已包含 mainline、内核和 Debian 配置仓库）：

```sh
repo init -u https://github.com/KawaiiHachimi/spark-android.git -b main -m manifests/base.xml
repo sync -c -j8
git clone https://github.com/KawaiiHachimi/spark-android.git ../spark-patches
python3 ../spark-patches/scripts/apply.py "$PWD" --check
python3 ../spark-patches/scripts/apply.py "$PWD" --apply
```

脚本校验基线和补丁 SHA256，先完整回放验证，再逐仓库 `git am`。原始提交号、补丁顺序及结果 tree 见 [sources.lock.json](sources.lock.json)；其他 mainline 仓库无需额外补丁，详见 [完整清单](docs/inventory.md)。

## 构建辅助

```sh
python3 ../spark-patches/scripts/install-support.py "$PWD"
python3 ../spark-patches/scripts/fetch-mesa-wraps.py "$PWD"
bash ../spark-patches/scripts/build-mesa-host-tools.sh "$PWD"
```

还需要匹配的 NVIDIA 610.43.03 固件和 arm64 EFI GRUB 主机工具，见 [构建与固件说明](docs/build-notes.md)。主机二进制、依赖缓存、固件及镜像未放入补丁仓库。

已验证全部补丁从干净基线回放后与整理的源码 tree 一致，见 [验证记录](docs/validation.json)。本次未重新全量编译或进行设备启动验证；补丁保留当前调试设置，包括 permissive SELinux、调试入口的 insecure ADB 和 `/data/vendor` 权限调整。
