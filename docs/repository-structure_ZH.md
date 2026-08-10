# 仓库结构

[English](repository-structure.md)

- `examples/esp-idf/`：6 个第一方 ESP-IDF 工程。
- `examples/arduino/`：9 个第一方 Arduino 草图及其捆绑库。
- `config/`：CI 策略和共享配置说明。
- `docs/`：第一方维护文档。
- `firmware/`：已发布出厂二进制，不进入默认示例 CI。
- `releases/`：源码构建示例工件的辅助脚本。
- `schematic/`：开发板原理图。
- `tests/`：示例发现、CI 路由、Markdown 策略与发布辅助工具的静态测试。
- `videos/`：文档引用的产品演示媒体。

正常示例矩阵不构建捆绑库示例或固件工程/工件。
