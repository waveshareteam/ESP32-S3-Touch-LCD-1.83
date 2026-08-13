# Components

[简体中文](components_ZH.md)

ESP-IDF examples use managed components where a supported product dependency exists, including `waveshare/esp32_s3_touch_lcd_1_83` and `waveshare/qmi8658` where declared by the example manifest.

The local `bsp_extra` directories remain intentionally: they wrap managed BSP codec functions and add product APIs used by the rich UI, spectrum-analyzer, and video examples. The applications remain first-party feature and UI code. `examples/arduino/libraries/Mylibrary/pin_config.h` is repository-local shared Arduino board configuration, not bundled upstream library content. Revisit this boundary only when a managed component provides equivalent product APIs and board behavior.

LVGL, ESP-Brookesia, ESP-DSP, AVI playback, JPEG decoding, and audio helpers are resolved through the ESP Component Registry according to each example manifest. The AXP2101 example intentionally keeps its small register-level implementation and depends only on ESP-IDF drivers.

Reusable fixes should be contributed upstream when practical. A local workaround should document the affected upstream version and remain only until a verified managed-component release provides equivalent behavior.
