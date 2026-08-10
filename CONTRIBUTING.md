# Contributing

[简体中文](CONTRIBUTING_ZH.md)

Thank you for helping improve this repository.

1. Open an issue or discussion before behavior changes that alter board support, example scope, CI policy, or delivered firmware.
2. Keep first-party ESP-IDF projects under `examples/esp-idf/` and Arduino sketches under `examples/arduino/`.
3. Keep bundled Arduino libraries as exact sketch dependencies; do not add their upstream examples to product CI.
4. Prefer managed ESP-IDF components for reusable board, display, touch, sensor, audio, and video support. Preserve product-specific wrappers until equivalence is proven.
5. Do not modify or repackage files below `firmware/` unless the pull request is an explicitly authorized firmware release update.

Run the repository Python tests, Markdown audit, routing audit, and `git diff --check` before opening a pull request. Run the relevant product build when the toolchain is available; otherwise state that it was not run and require the complete current-head Actions matrix.

The pull request should identify the affected board revision, example paths, framework versions, validation results, and any pin, BSP, component, or firmware impact. Use repository-relative paths and remove credentials, personal data, device identifiers, and machine-specific paths from logs.
