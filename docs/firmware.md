# Firmware artifacts

[简体中文](firmware_ZH.md)

[`firmware/`](../firmware/) contains the published factory image for flashing and recovery. It is immutable delivery material: routine documentation and CI work must not rebuild, repackage, rename, or modify it.

The example workflow builds only first-party projects under `examples/` and may package source-built diagnostic artifacts. Those artifacts are not factory firmware and do not validate or replace it. Source and build instructions for other firmware surfaces are not included here and may be added in a later update.

The [release helpers](../releases/README.md) create per-example archives from build outputs and can download artifacts from a selected GitHub Actions run. They write only to their configured output directories and never update the checked-in factory image.
