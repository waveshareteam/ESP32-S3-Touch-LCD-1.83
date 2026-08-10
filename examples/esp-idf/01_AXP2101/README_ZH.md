# AXP2101 PMU 示例

[English](README.md)

此示例通过 I2C 初始化 AXP2101 电源管理 IC，并输出稳压器、电池、VBUS、充电器和系统电压状态。

示例使用 `main/port_axp2101.cpp` 中的小型本地 AXP2101 寄存器驱动程序，以及 `main/axp2101_registers.h` 中的寄存器定义；未包含完整的多芯片 XPowersLib 副本。

## 构建

```bash
idf.py -C examples/esp-idf/01_AXP2101 set-target esp32s3 build
```

默认引脚：

- PMU I2C SCL：GPIO 14
- PMU I2C SDA：GPIO 15
- PMU 状态处理：由示例任务轮询

如果开发板修订版改变了接线，请在 menuconfig 的 `AXP2101 PMU Configuration` 中调整 I2C 参数。
