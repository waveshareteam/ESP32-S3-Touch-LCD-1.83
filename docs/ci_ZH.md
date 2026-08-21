# CI

[English](ci.md)

`Build Examples` 工作流会在拉取请求和受支持的推送中始终运行 `Scope and static checks` 任务。它会在昂贵矩阵之前运行仓库 Python 测试、YAML 解析、不可变工件检查、Markdown 审计和改动文件路由审计。在验证完整基线提交后，它会对同一完整范围运行 `git diff --check`。

矩阵包含 6 个第一方 ESP-IDF 工程，分别使用 `v5.5.5` 与 `v6.0.2`（共 12 项），以及 9 个使用 Arduino-ESP32 `3.3.11` 和 `esp32:esp32:esp32s3:FlashMode=qio,FlashSize=16M,PSRAM=opi,USBMode=hwcdc,PartitionScheme=default` 的第一方 Arduino 草图。ESP32-S3R8 板使用 16 MB Flash、八线 PSRAM、QIO 模式和默认分区方案。捆绑 Arduino 库示例和 `firmware/` 中的所有文件均不进入默认示例矩阵。

对于拉取请求和分支推送，完整且支持重命名的差异决定选择范围：文档不选择示例；直接示例修改仅选择对应工程或草图；共享框架或构建输入选择相应的完整集合。空或不可用的差异会失败关闭。路由报告会导出 `docs_only`、`firmware_touched` 和 `release_review_required`，范围任务会发布供审阅者使用的通用摘要；仅固件文档改动不会使任务失败。手动运行和标签运行始终选择完整的 12 项 ESP-IDF 与 9 项 Arduino 矩阵。拉取请求和分支验证可由更新的运行取消；手动和标签运行会保留且不会被取消。

已提交交付工件依据 `config/immutable-artifacts.sha256` 验证。经维护者批准的发布必须同时修改工件和清单；普通拉取请求会因摘要不匹配或未列出的受跟踪固件二进制文件而失败。

每个成功的矩阵项都会上传源码构建诊断压缩包。这些压缩包与已提交的出厂固件严格分离；内容和下载流程请参阅[发布辅助工具文档](../releases/README_ZH.md)。
