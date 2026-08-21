# 发布辅助工具

[English](README.md)

此目录包含源码构建示例输出的打包工具和 CI 工件下载工具。生成的压缩包是示例诊断工件，不是出厂固件，也不得作为产品交付文件提交。

## ESP-IDF 打包

构建示例后，对其构建目录进行打包：

```bash
idf.py -C examples/esp-idf/02_lvgl_demo_v9 \
  -B build/02_lvgl_demo_v9-v6.0.2 set-target esp32s3 build

python3 releases/package_firmware.py \
  --framework esp-idf \
  --project examples/esp-idf/02_lvgl_demo_v9 \
  --build-dir build/02_lvgl_demo_v9-v6.0.2 \
  --framework-version v6.0.2 \
  --target esp32s3
```

辅助工具读取 ESP-IDF 的 `flasher_args.json`，复制所需二进制文件，生成刷写脚本，并在 `releases/dist/` 下创建压缩包。

## Arduino 打包

将 Arduino 草图导出到稳定输出目录，然后打包：

```bash
arduino-cli compile \
  --fqbn esp32:esp32:esp32s3:FlashMode=qio,FlashSize=16M,PSRAM=opi,USBMode=hwcdc,PartitionScheme=default \
  --libraries examples/arduino/libraries \
  --export-binaries \
  --output-dir build/01_HelloWorld-3.3.11 \
  examples/arduino/01_HelloWorld

python3 releases/package_firmware.py \
  --framework arduino \
  --project examples/arduino/01_HelloWorld \
  --build-dir build/01_HelloWorld-3.3.11 \
  --framework-version 3.3.11 \
  --target esp32s3
```

每个压缩包包含 `manifest.json`、`flash.sh`、`flash.bat`、`flash_args.txt`，以及 `bin/` 下所需的二进制文件。

## 下载 CI 工件

下载并解压已完成的工作流运行：

```bash
python3 releases/download_artifacts.py --run-id <run-id> --clean
```

省略 `--run-id` 时，辅助工具会查找当前分支最新成功的 `examples.yml` 运行：

```bash
python3 releases/download_artifacts.py --clean
```

使用 `--artifact <name>` 选择单个工件，或使用 `--pattern "firmware-esp-idf-*v6.0.2"` 进行 glob 筛选。辅助工具使用 `GH_TOKEN`、`GITHUB_TOKEN` 或 `gh auth token`。解压后的文件写入已被 Git 忽略的 `releases/downloads/run-<run-id>/`。

[`firmware/`](../firmware/) 中已提交的镜像是独立的不可变交付表面；这些辅助工具不会重新构建或替换它。经维护者批准的发布改动必须同时更新工件及其不可变清单；普通拉取请求会因哈希检查失败而被阻止。
