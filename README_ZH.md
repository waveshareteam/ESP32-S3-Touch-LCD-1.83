<div align="center">
  <h1>ESP32-S3-Touch-LCD-1.83</h1>
  <p><strong>ESP32-S3 1.83 英寸 240 × 284 IPS 电容触摸开发板</strong></p>
  <p>
    <a href="https://github.com/waveshareteam/ESP32-S3-Touch-LCD-1.83/actions/workflows/examples.yml"><img alt="Build Examples" src="https://github.com/waveshareteam/ESP32-S3-Touch-LCD-1.83/actions/workflows/examples.yml/badge.svg"></a>
    <a href="https://github.com/waveshareteam/ESP32-S3-Touch-LCD-1.83/releases/latest"><img alt="Latest Release" src="https://img.shields.io/github/v/release/waveshareteam/ESP32-S3-Touch-LCD-1.83"></a>
    <a href="LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/waveshareteam/ESP32-S3-Touch-LCD-1.83"></a>
  </p>
  <p><a href="README.md">English</a></p>
  <p><img src="assets/images/ESP32-S3-Touch-LCD-1.83.jpg" alt="ESP32-S3-Touch-LCD-1.83 带外壳和显示屏的开发板" width="520"></p>
  <p>
    <a href="https://www.waveshare.com/product/esp32-s3-touch-lcd-1.83.htm">🌐 产品页</a> |
    <a href="https://docs.waveshare.com/ESP32-S3-Touch-LCD-1.83">📚 产品文档</a> |
    <a href="firmware/">📦 出厂固件</a> |
    <a href="examples/esp-idf/">🧩 ESP-IDF</a> |
    <a href="examples/arduino/">🔧 Arduino</a>
  </p>
</div>

---

## ✨ 概述

本仓库提供 ESP32-S3-Touch-LCD-1.83 的第一方 ESP-IDF 与 Arduino 示例、出厂恢复固件、原理图、视频资源和维护文档。

该开发板将 ESP32-S3 与小尺寸显示和触摸接口、电源管理、运动传感器、实时时钟、音频、microSD 存储和 USB 连接集成在一起。

## 🖥️ 硬件概览

| 功能 | 器件 / 接口 |
| --- | --- |
| MCU | ESP32-S3R8，8 MB PSRAM 和 16 MB Flash |
| 显示 | 1.83 英寸 240 × 284 IPS LCD，通过 SPI 连接 ST7789P |
| 触摸 | CST816 系列电容触摸控制器，通过 I2C 连接 |
| 电源管理 | AXP2101 |
| 运动传感器 | QMI8658 六轴 IMU |
| RTC | PCF85063 |
| 音频 | ES8311 编解码器和 ES7210 ADC |
| 存储与连接 | microSD、USB、I2C 和 UART |
| 板级支持 | 托管组件 `waveshare/esp32_s3_touch_lcd_1_83` |
| 硬件文件 | [原理图](schematic/)和[视频资源](videos/) |

硬件相关改动必须依据原理图验证；构建成功只能证明可编译，不能证明引脚配置正确。

## 📦 固件与恢复

[`firmware/`](firmware/) 包含已提交的出厂恢复镜像。它是不可变交付物，不是源码工程，也不参与示例 CI。常规文档和 CI 改动不得重新构建、打包、重命名或修改它。

CI 源码构建工件仅用于所选示例的诊断，不能替代或验证出厂固件。参阅[固件说明](docs/firmware_ZH.md)。

## 🧪 示例

### ESP-IDF

| 示例 | 重点 |
| --- | --- |
| [01_AXP2101](examples/esp-idf/01_AXP2101/) | 电源管理与电池遥测 |
| [02_lvgl_demo_v9](examples/esp-idf/02_lvgl_demo_v9/) | LVGL 9 显示示例 |
| [03_esp-brookesia](examples/esp-idf/03_esp-brookesia/) | ESP-Brookesia 应用界面 |
| [04_Immersive_block](examples/esp-idf/04_Immersive_block/) | 运动驱动交互示例 |
| [05_Spec_Analyzer](examples/esp-idf/05_Spec_Analyzer/) | 音频频谱分析器 |
| [06_videoplayer](examples/esp-idf/06_videoplayer/) | 视频播放 |

### Arduino

| 示例 | 重点 |
| --- | --- |
| [01_HelloWorld](examples/arduino/01_HelloWorld/) | 显示初始化 |
| [02_Drawing_board](examples/arduino/02_Drawing_board/) | 触摸绘图 |
| [03_GFX_AsciiTable](examples/arduino/03_GFX_AsciiTable/) | GFX 文本渲染 |
| [04_GFX_ESPWiFiAnalyzer](examples/arduino/04_GFX_ESPWiFiAnalyzer/) | Wi-Fi 扫描可视化 |
| [05_GFX_Clock](examples/arduino/05_GFX_Clock/) | 时钟显示 |
| [06_GFX_PCF85063_simpleTime](examples/arduino/06_GFX_PCF85063_simpleTime/) | PCF85063 RTC 显示 |
| [07_LVGL_PCF85063_simpleTime](examples/arduino/07_LVGL_PCF85063_simpleTime/) | LVGL RTC 界面 |
| [08_LVGL_QMI8658_ui](examples/arduino/08_LVGL_QMI8658_ui/) | LVGL IMU 数据界面 |
| [09_LVGL_Arduino](examples/arduino/09_LVGL_Arduino/) | LVGL 触摸界面 |

捆绑 Arduino 库位于 [`examples/arduino/libraries/`](examples/arduino/libraries/)。其中的上游示例可供参考，但不是第一方产品 CI 目标。

## 🛠️ 工具链与 CI

CI 使用 ESP-IDF `v5.5.5` 与 `v6.0.2` 构建全部 6 个 ESP-IDF 工程，并使用 Arduino-ESP32 `3.3.11` 和 `esp32:esp32:esp32s3` 构建全部 9 个 Arduino 草图。

每个拉取请求都会得到轻量范围与静态检查结果。仅文档改动不选择产品构建；直接修改示例只选择受影响工程或草图；共享构建输入选择相应完整矩阵。差异为空或不可用时会失败关闭。参阅 [CI 文档](docs/ci_ZH.md)。

## 🗂️ 仓库结构

| 路径 | 用途 |
| --- | --- |
| [`examples/esp-idf/`](examples/esp-idf/) | 第一方 ESP-IDF 工程 |
| [`examples/arduino/`](examples/arduino/) | 第一方 Arduino 草图与捆绑库 |
| [`config/`](config/) | CI 策略与共享配置 |
| [`docs/`](docs/) | 仓库、CI、组件、固件和兼容性说明 |
| [`firmware/`](firmware/) | 不可变出厂刷写与恢复镜像 |
| [`releases/`](releases/) | 源码构建示例工件辅助工具 |
| [`schematic/`](schematic/) | 公开原理图 |
| [`videos/`](videos/) | 视频示例使用的媒体资源 |

## 📚 文档与支持

- [仓库结构](docs/repository-structure_ZH.md)
- [持续集成](docs/ci_ZH.md)
- [组件](docs/components_ZH.md)
- [固件工件](docs/firmware_ZH.md)
- [ESP-Brookesia 说明](docs/brookesia_ZH.md)
- [发布辅助工具](releases/README_ZH.md)
- [贡献指南](CONTRIBUTING_ZH.md)
- [支持](SUPPORT_ZH.md)
- [安全策略](SECURITY_ZH.md)
- [提交 Issue](https://github.com/waveshareteam/ESP32-S3-Touch-LCD-1.83/issues/new/choose)

## 📄 许可证

本仓库采用 Apache License 2.0，详见 [LICENSE.txt](LICENSE.txt)。
