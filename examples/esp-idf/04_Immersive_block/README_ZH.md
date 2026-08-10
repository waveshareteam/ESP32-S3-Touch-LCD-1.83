# 沉浸式方块示例

[English](README.md)

此 ESP-IDF 示例面向 `esp32s3`，使用 LVGL 显示随机生成的形状。QMI8658 加速度计控制形状移动，碰撞处理和圆角屏幕边界使形状保持在显示区域内。

首次校准时请将开发板放在水平表面上。按下 BOOT 按钮（GPIO0）可再次请求校准。

## 依赖项

组件清单声明以下依赖项：

- ESP-IDF `>=5.5.0`
- `waveshare/qmi8658` `^2.0.0`
- `waveshare/esp32_s3_touch_lcd_1_83` `^2.0.0`
- `lvgl/lvgl` `^9.2.0`

声明的版本见 [`main/idf_component.yml`](main/idf_component.yml)。工程目标和默认配置见 [`sdkconfig.defaults`](sdkconfig.defaults)。

## 构建

在仓库根目录运行以下命令构建工程：

```bash
idf.py -C examples/esp-idf/04_Immersive_block set-target esp32s3 build
```

应用程序入口为 [`main/main.c`](main/main.c)。
