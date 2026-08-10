# Repository structure

[简体中文](repository-structure_ZH.md)

- `examples/esp-idf/`: six first-party ESP-IDF projects.
- `examples/arduino/`: nine first-party Arduino sketches and their bundled libraries.
- `config/`: CI policy and shared configuration documentation.
- `assets/images/`: official product visual assets used by the homepage.
- `docs/`: first-party maintenance documentation.
- `firmware/`: published factory binary, outside default example CI.
- `releases/`: helper scripts for source-built example artifacts.
- `schematic/`: board schematic.
- `tests/`: static tests for discovery, CI routing, Markdown policy, and release helpers.
- `videos/`: product demonstration media referenced by the documentation.

The normal example matrix does not build bundled-library examples or firmware projects/artifacts.
