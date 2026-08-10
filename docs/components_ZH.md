# 组件

[English](components.md)

ESP-IDF 示例在已声明且受支持时使用托管组件，包括 `waveshare/esp32_s3_touch_lcd_1_83` 与 `waveshare/qmi8658`。

本地 `bsp_extra` 目录被有意保留：它们是富 UI、频谱分析器和视频示例使用的产品音频及板级粘合代码。尚未证明存在等价托管组件行为，因此不会进行推测性替换。

LVGL、ESP-Brookesia、ESP-DSP、AVI 播放、JPEG 解码与音频辅助组件按照各示例清单从 ESP Component Registry 解析。AXP2101 示例有意保留精简的寄存器级实现，并且只依赖 ESP-IDF 驱动。

可复用修复应尽量回馈上游。本地变通方案应注明受影响的上游版本，并仅保留到经验证的托管组件版本提供等价行为为止。
