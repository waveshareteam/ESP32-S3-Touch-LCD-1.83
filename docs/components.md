# Components

Prefer managed components for reusable board support, display, touch, sensor, audio, and video code.

Current managed component policy:

- `waveshare/esp32_s3_touch_lcd_1_83` is the board support package for ESP-IDF examples.
- `waveshare/qmi8658` is used by the IMU example.
- LVGL, ESP-Brookesia, ESP-DSP, AVI playback, JPEG, and audio helper components are resolved through the ESP Component Manager where examples already use them.
- `bsp_extra` remains local because it is board-specific audio glue used by the rich UI, spectrum analyzer, and video examples.
- The AXP2101 example uses a minimal local register driver instead of carrying the full multi-chip XPowersLib copy.

If a local workaround becomes generally useful, move it to the shared component repository first, then update this product repository to consume the released managed component.
