# 固件

[English](README.md) | [简体中文](README_ZH.md)

ESP32-S3-Touch-LCD-1.83 的出厂固件。BIN 同时包含出厂演示和小智 AI，是从 `0x0` 烧录的合并镜像，文件名中的日期即版本。

| 文件 | 用途 |
| --- | --- |
| [ESP32-S3-Touch-LCD-1.83_FactoryOnly_20251024.bin](ESP32-S3-Touch-LCD-1.83_FactoryOnly_20251024.bin) | 出厂演示与小智 AI 组合固件 |

在本目录运行以下命令，将 `<PORT>` 替换为开发板对应的串口。整片擦除会清除已有设置和用户数据。

```bash
python -m pip install esptool
esptool.py --chip esp32s3 --port <PORT> erase_flash
esptool.py --chip esp32s3 --port <PORT> write_flash 0x0 ESP32-S3-Touch-LCD-1.83_FactoryOnly_20251024.bin
```
