# Immersive Block Example

[简体中文](README_ZH.md)

This ESP-IDF example targets `esp32s3` and uses LVGL to display randomly generated shapes. The QMI8658 accelerometer controls their movement, while collision handling and rounded-screen bounds keep the shapes on the display.

Place the board on a level surface during the initial calibration. Press the BOOT button (GPIO0) to request calibration again.

## Dependencies

The component manifest lists these dependencies:

- ESP-IDF `>=5.5.0`
- `waveshare/qmi8658` `^2.0.0`
- `waveshare/esp32_s3_touch_lcd_1_83` `^2.0.0`
- `lvgl/lvgl` `^9.2.0`

See [`main/idf_component.yml`](main/idf_component.yml) for the declared versions. The project target and defaults are in [`sdkconfig.defaults`](sdkconfig.defaults).

## Build

From the repository root, build the project with:

```bash
idf.py -C examples/esp-idf/04_Immersive_block set-target esp32s3 build
```

The application entry point is [`main/main.c`](main/main.c).
