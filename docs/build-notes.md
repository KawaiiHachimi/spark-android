# 构建与固件说明

## 基线及范围

- 基线使用本次整理前的上游提交，未更新任何上游分支；主 manifest 为 LineageOS `lineage-24.0`，Mesa 及其构建依赖使用本地 manifest 原有的 `lineage-23.2` 基线。
- `manifests/base.xml` 锁定全部项目，并补上原源码树中未由 repo 管理的 `kernel/mainline/android-mainline` 和 `external/debian-linux`。`manifests/02-mainline.xml` 是原始 mainline 依赖配置，供已有源码树参考；不要与完整基线 manifest 重复加载。
- `sources.lock.json` 中的 `head` 是本地整理提交，尚未推送到各上游仓库；通过补丁重建。`git am` 的提交号可能因 committer 元数据不同而变化，最终 tree 应一致。
- 原有 device 文档中的额外 Gerrit topics 是上游通用适配说明。本补丁集只打包当前源码树实际存在的差异，未自动抓取或补打文档中列出的其他改动。
- `build/make`、`build/soong` 是当前构建主机的 JVM 调整；device 的文档维护、kernel 的 SELinux/virtio 补丁属于通用 mainline 配套改动。全部保留，便于还原当前状态。
- Mesa 的 nvgpu 后端和 Tegra/Freedreno 兼容改动也属于现有差异；Spark 此处使用 Nouveau/NVK 路径，未单独验证 nvgpu 后端。

## Mesa 26.2.2

升级提交来自 [官方源码归档](https://archive.mesa3d.org/mesa-26.2.2.tar.xz)，SHA256：

```text
eeb29ca7e56cfaa8e8a79538dcf834e3b18e501c31bef5145e959ea437cc4216
```

第一个补丁导入 release 源码并保留原有 `lineage.dependencies`；后续三个补丁分别保留 AOSP 构建集成、NVK/nvgpu 修改和其他兼容/离线依赖修改。该升级包含完整上游源码差异，因此也包括上游测试资源。

当前 `.wrap` 已去掉下载 URL，并使用 `subprojects/packagefiles/`。`scripts/fetch-mesa-wraps.py` 根据 `support/mesa-wraps.json` 从原 URL 下载并校验 40 个归档，无需把缓存加入 Git；可加 `--check` 仅校验现有文件。对应的 Meson 源码补丁已随系列打包。

`scripts/install-support.py` 安装原有 Rust wrapper，替换其中的本机绝对路径，并重建两个指向 Android 产出 `libc++.vendor.so` 的 Clang 搜索路径符号链接。库本体由 Android 构建生成，不应提交进 prebuilts。wrapper 处理 AOSP rustc 的 `-dev` 版本后缀以及 Android target 的 `panic=abort`。

`mesa-host-tools/bin/` 中的四个现有 ELF 工具不进入 Git。`scripts/build-mesa-host-tools.sh` 提供从当前 Mesa 源码重建 `vtn_bindgen2`、`asahi_clc`、`panfrost_compile` 和 `pco_clc` 的命令；需要独立的 x86_64 Mesa 编译环境，包括 LLVM/Clang 开发库、libclc、Rust/bindgen/cbindgen、Meson/Ninja 和 Python Mako/PyYAML。应使用主机 Rust，避免把 Android wrapper 加入该原生工具构建的 PATH。该重建脚本本次只做语法检查，未重新执行构建；原工具哈希见 `support/host-tools.json`。

Mesa Android 构建还固定引用 Clang `clang-r584948` 的 bindgen 内建头文件、`clang-r596125` runtime 和 Rust `1.93.1`。这些由精确基线提供；换用其他分支时需要相应调整补丁。

## GB20B 固件

内核补丁匹配 NVIDIA **610.43.03**。现有固件镜像中存在：

```text
nvidia/gb20b/gsp/bootloader-610.43.03.bin
nvidia/gb20b/gsp/fmc-610.43.03.bin
nvidia/gb20b/gsp/gsp-610.43.03.bin
nvidia/gb20b/gsp/ucodes-610.43.03.bin
```

原始 `external/linux-firmware-mainline` 仓库没有源码修改；上述额外文件位于现有 `out/linux-firmware.img` 中。本仓库只记录这些文件的校验值（`support/firmware.json`），不分发固件二进制。

使用 [NVIDIA OpenRM 610.43.03](https://github.com/NVIDIA/open-gpu-kernel-modules/tree/610.43.03) 及配套的固件提取脚本。辅助脚本的调用方式：

```sh
python3 nvk-rust-bin/extract-gb20b-610.py /path/to/extraction-script.py /path/to/openrm-source /path/to/firmware-output
```

传入的提取脚本需提供 `gsp_bootloader()` 和 `fmc()`；OpenRM 目录需包含匹配版本的 GB20B GspRmBoot 和 production FMC generated C 文件。再从匹配版本的 `.run` 固件目录分别复制 `gsp_ga10x.bin`、`ucodes_ga10x.bin` 并按上面的名字放入 firmware 根目录。保留基础 linux-firmware 内容，用 `mkfs.erofs` 制作镜像，构建时设置 `TARGET_LINUX_FIRMWARE_IMAGE`。该辅助脚本本次未重新提取固件。

## Live ISO

arm64 ISO 补丁在 x86_64 主机调用 `/usr/bin/grub-mkrescue`、`/usr/lib/grub/arm64-efi`，需安装相应 GRUB arm64 EFI 模块和 xorriso。例如 Debian/Ubuntu 对应 `grub-common`、`grub-efi-arm64-bin`、`xorriso`，具体安装命令按构建主机发行版处理。

```sh
source build/envsetup.sh
lunch lineage_Generic_arm64-userdebug
export TARGET_LINUX_FIRMWARE_IMAGE=/absolute/path/to/linux-firmware.img
m liveisoimage
```

以上是构建入口参考；本次未重新运行全量 Android 构建。现有产出为 2026-09-18 的 Generic_arm64 Live ISO，产出文件存在不能证明当前补丁已通过设备启动测试。

## 排除项与验证

未提交下载归档、解压依赖、`.wraplock`、Python `__pycache__`、`out/`、日志和主机 ELF。Clang 的两个未跟踪软链接由安装辅助脚本处理，`prebuilts/mesa-build-dep` 的未跟踪文件均为 Python 缓存。其余 mainline 仓库和 Debian 配置仓库保持干净，基线见 `inventory.md`。

`scripts/apply.py --verify-package` 在临时索引中从各仓库基线应用完整补丁系列，并比较最终 tree；不修改源码工作区。全部 9 个仓库、16 个补丁通过，另有 40 个依赖归档校验通过。原源码树的已跟踪文件均已整理为本地 `spark-android` 分支提交。未执行全量重编译、固件重提取或设备启动验证。

补丁中的原始版权和许可证声明保持不变，各改动遵循对应上游文件的许可证。
