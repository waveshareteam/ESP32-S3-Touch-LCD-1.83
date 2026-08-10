# Release helpers

[简体中文](README_ZH.md)

This directory contains helpers for packaging source-built example outputs and downloading CI artifacts. Generated archives are diagnostics for examples; they are not factory firmware and must not be committed as product delivery files.

## ESP-IDF packaging

After building an example, package its build directory:

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

The helper reads ESP-IDF's `flasher_args.json`, copies the required binaries, writes flash helpers, and creates an archive below `releases/dist/`.

## Arduino packaging

Export an Arduino sketch into a stable output directory, then package it:

```bash
arduino-cli compile \
  --fqbn esp32:esp32:esp32s3 \
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

Each archive contains `manifest.json`, `flash.sh`, `flash.bat`, `flash_args.txt`, and the required binaries below `bin/`.

## Downloading CI artifacts

Download and extract one completed workflow run:

```bash
python3 releases/download_artifacts.py --run-id <run-id> --clean
```

Without `--run-id`, the helper finds the latest successful `examples.yml` run for the current branch:

```bash
python3 releases/download_artifacts.py --clean
```

Use `--artifact <name>` for one artifact or `--pattern "firmware-esp-idf-*v6.0.2"` for a glob selection. The helper uses `GH_TOKEN`, `GITHUB_TOKEN`, or `gh auth token`. Extracted files are written below `releases/downloads/run-<run-id>/`, which is ignored by Git.

The checked-in image in [`firmware/`](../firmware/) is a separate immutable delivery surface. These helpers never rebuild or replace it.
