# Waveshare ESP32-S3-Touch-LCD-1.83

ESP32-S3-Touch-LCD-1.83 is a compact Waveshare development board with an ESP32-S3 MCU, 1.83-inch capacitive LCD, power management, six-axis motion sensor, RTC, and low-power audio codec.

## Repository Layout

- `examples/esp-idf/`: first-party ESP-IDF projects.
- `examples/arduino/`: first-party Arduino sketches and bundled libraries.
- `config/`: shared configuration overlays.
- `docs/`: maintainer notes for structure, CI, components, firmware, and Brookesia.
- `firmware/`: released factory binary artifacts, excluded from build CI.
- `releases/`: scripts for packaging CI and local build outputs into flashable firmware archives.
- `schematic/`: hardware schematic files.
- `videos/`: media assets for video playback examples.

## ESP-IDF Examples

Build ESP-IDF examples with target `esp32s3`:

```bash
idf.py -C examples/esp-idf/02_lvgl_demo_v9 set-target esp32s3 build
```

CI covers first-party ESP-IDF examples with ESP-IDF `v5.5.4` and `v6.0.2`.

## Arduino Examples

First-party sketches live directly under `examples/arduino/`. Bundled libraries live under `examples/arduino/libraries/` and are used by the sketches.

```bash
arduino-cli compile --fqbn esp32:esp32:esp32s3 --libraries examples/arduino/libraries examples/arduino/01_HelloWorld
```

CI compiles first-party sketches with Arduino-ESP32 core `3.3.10`. Examples inside bundled libraries are intentionally excluded from product CI.

## Documentation

- [Repository structure](docs/repository-structure.md)
- [CI](docs/ci.md)
- [Components](docs/components.md)
- [Firmware artifacts](docs/firmware.md)
- [ESP-Brookesia notes](docs/brookesia.md)

For product setup details, refer to the Waveshare product wiki.

## Support

Use GitHub issues for repository problems. Include the example path, framework version, and build or runtime logs. For product support, contact Waveshare support channels and provide the order number when needed.

## License

This repository is licensed under the Apache License. See `LICENSE.txt` for details.
