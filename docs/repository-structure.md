# Repository Structure

This repository uses the Waveshare ESP32 product layout:

- `examples/esp-idf/`: first-party ESP-IDF projects for the ESP32-S3 Touch LCD 1.83 board.
- `examples/arduino/`: first-party Arduino sketches plus bundled libraries required by those sketches.
- `config/`: shared configuration overlays used by more than one example.
- `docs/`: maintainer notes for CI, components, firmware, and compatibility.
- `firmware/`: factory binary artifacts that are documented but not built in CI.
- `releases/`: scripts for packaging build outputs into flashable firmware archives.
- `schematic/`: public schematic files.
- `videos/`: media assets used by video playback examples.

CI intentionally builds only first-party examples. Examples and tests inside bundled Arduino libraries remain available for library users, but they are not product CI targets.
