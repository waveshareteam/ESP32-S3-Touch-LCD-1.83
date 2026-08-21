# CI

[简体中文](ci_ZH.md)

The `Build Examples` workflow always runs its `Scope and static checks` job on pull requests and supported pushes. It runs the repository's Python tests, YAML parsing, immutable-artifact checker, Markdown audit, and changed-file routing audit before any expensive matrix job. After validating the complete base revision, it runs `git diff --check` on the same complete range.

The matrix contains six first-party ESP-IDF projects on `v5.5.5` and `v6.0.2` (12 entries) and nine first-party Arduino sketches on Arduino-ESP32 `3.3.11` with `esp32:esp32:esp32s3:FlashMode=qio,FlashSize=16M,PSRAM=opi,USBMode=hwcdc,PartitionScheme=default`. The ESP32-S3R8 board uses 16 MB flash, octal PSRAM, QIO mode, and the default partition scheme. Bundled Arduino library examples and every file under `firmware/` remain outside the default example matrix.

For pull requests and branch pushes, a complete rename-aware diff drives selection: documentation selects no examples; a direct example edit selects only that project or sketch; shared framework/build inputs select the applicable full set. Empty or unavailable diff data fails closed. The routing report exports `docs_only`, `firmware_touched`, and `release_review_required`, and the scope job publishes a generic summary for reviewers; firmware documentation alone does not fail the job. Manual runs and tags always select the complete 12-entry ESP-IDF and 9-entry Arduino matrices. Pull request and branch validation runs may be cancelled by newer runs, while manual and tag runs are retained.

Checked-in delivery artifacts are verified against `config/immutable-artifacts.sha256`. A maintainer-approved release changes the artifact and manifest together; ordinary pull requests fail on a digest mismatch or an unlisted tracked firmware binary.

Each successful matrix entry uploads a source-built diagnostic archive. These archives are separate from checked-in factory firmware; see the [release helper documentation](../releases/README.md) for their contents and download flow.
