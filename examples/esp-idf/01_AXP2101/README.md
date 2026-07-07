# AXP2101 PMU Example

This example initializes the AXP2101 power-management IC over I2C and prints regulator, battery, VBUS, charger, and system-voltage status.

The example uses a small local AXP2101 register driver in `main/port_axp2101.cpp` plus register definitions in `main/axp2101_registers.h`. It does not carry the full multi-chip XPowersLib copy.

## Build

```bash
idf.py -C examples/esp-idf/01_AXP2101 set-target esp32s3 build
```

Default pins:

- PMU I2C SCL: GPIO 14
- PMU I2C SDA: GPIO 15
- PMU status handling: polled by the example task

Adjust the I2C values from menuconfig under `AXP2101 PMU Configuration` if a board revision changes the wiring.
