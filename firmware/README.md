# Firmware

[English](README.md) | [简体中文](README_ZH.md)

Factory firmware for ESP32-S3-Touch-LCD-1.83. The BIN is a merged image containing both the factory demo and Xiaozhi AI, flashed at `0x0`; the date in its file name identifies the version.

| File | Purpose |
| --- | --- |
| [ESP32-S3-Touch-LCD-1.83_FactoryOnly_20251024.bin](ESP32-S3-Touch-LCD-1.83_FactoryOnly_20251024.bin) | Combined factory demo and Xiaozhi AI firmware |

Run these commands in this directory, replacing `<PORT>` with the board's serial port. Erasing flash removes existing settings and user data.

```bash
python -m pip install esptool
esptool.py --chip esp32s3 --port <PORT> erase_flash
esptool.py --chip esp32s3 --port <PORT> write_flash 0x0 ESP32-S3-Touch-LCD-1.83_FactoryOnly_20251024.bin
```
