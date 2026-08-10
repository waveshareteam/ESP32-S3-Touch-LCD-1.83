# CI

[简体中文](ci_ZH.md)

The `Build Examples` workflow always runs its `Scope and static checks` job on pull requests and supported pushes. It runs the repository's Python tests, YAML parsing, Markdown audit, and changed-file routing audit before any expensive matrix job.

The matrix contains six first-party ESP-IDF projects on `v5.5.5` and `v6.0.2` (12 entries) and nine first-party Arduino sketches on Arduino-ESP32 `3.3.11`. Bundled Arduino library examples and every file under `firmware/` remain outside the default example matrix.

For pull requests and branch pushes, a complete rename-aware diff drives selection: documentation selects no examples; a direct example edit selects only that project or sketch; shared framework/build inputs select the applicable full set. Empty or unavailable diff data fails closed. Manual runs and tags always select the complete 12-entry ESP-IDF and 9-entry Arduino matrices. Pull request and branch validation runs may be cancelled by newer runs, while manual and tag runs are retained.

Each successful matrix entry uploads a source-built diagnostic archive. These archives are separate from checked-in factory firmware; see the [release helper documentation](../releases/README.md) for their contents and download flow.
