#include <Arduino.h>
#include "Arduino_GFX_Library.h"
#include "pin_config.h"
#include "SensorPCF85063.hpp"
#include <Wire.h>

#include "HWCDC.h"
HWCDC USBSerial;

SensorPCF85063 rtc;
uint32_t lastMillis;
char previousDateString[12] = "";
char previousTimeString[10] = "";
Arduino_DataBus *bus = new Arduino_ESP32SPI(LCD_DC, LCD_CS, LCD_SCK, LCD_MOSI);

Arduino_GFX *gfx = new Arduino_ST7789(bus, LCD_RST /* RST */,
                                      0 /* rotation */, true /* IPS */, LCD_WIDTH, LCD_HEIGHT, 0, 0, 0, 0);

static int16_t getTextWidth(const char *text, uint8_t textSize) {
  return strlen(text) * 6 * textSize;
}

static int16_t getCenteredX(const char *text, uint8_t textSize) {
  int16_t textWidth = getTextWidth(text, textSize);
  if (textWidth >= LCD_WIDTH) {
    return 0;
  }
  return (LCD_WIDTH - textWidth) / 2;
}

static void drawCenteredText(const char *text, uint8_t textSize, int16_t y, uint16_t color) {
  gfx->setTextColor(color);
  gfx->setTextSize(textSize, textSize, 0);
  gfx->setCursor(getCenteredX(text, textSize), y);
  gfx->print(text);
}

static void drawStaticUi() {
  gfx->fillScreen(WHITE);
  drawCenteredText("PCF85063 RTC", 2, 28, BLACK);
  drawCenteredText("Waveshare", 2, 56, BLUE);
  gfx->fillRect(20, 86, LCD_WIDTH - 40, 2, 0xC618);
  gfx->fillRect(20, 210, LCD_WIDTH - 40, 2, 0xC618);
}

void setup() {
  USBSerial.begin(115200);
  if (!rtc.begin(Wire, PCF85063_SLAVE_ADDRESS, IIC_SDA, IIC_SCL)) {
    USBSerial.println("Failed to find PCF8563 - check your wiring!");
    while (1) {
      delay(1000);
    }
  }

  uint16_t year = 2025;
  uint8_t month = 10;
  uint8_t day = 23;
  uint8_t hour = 15;
  uint8_t minute = 03;
  uint8_t second = 00;

  rtc.setDateTime(year, month, day, hour, minute, second);
  gfx->begin();
  pinMode(LCD_BL, OUTPUT);
  digitalWrite(LCD_BL, HIGH);
  drawStaticUi();
}

void loop() {
  if (millis() - lastMillis > 1000) {
    lastMillis = millis();

    RTC_DateTime datetime = rtc.getDateTime();
    char dateString[12];
    char timeString[10];
    snprintf(dateString, sizeof(dateString), "%04d-%02d-%02d", datetime.year, datetime.month, datetime.day);
    snprintf(timeString, sizeof(timeString), "%02d:%02d:%02d", datetime.hour, datetime.minute, datetime.second);

    if (strcmp(dateString, previousDateString) != 0 || strcmp(timeString, previousTimeString) != 0) {
      gfx->fillRect(0, 100, LCD_WIDTH, 92, WHITE);
      drawCenteredText(dateString, 2, 102, BLACK);
      drawCenteredText(timeString, 4, 132, BLUE);
      strcpy(previousDateString, dateString);
      strcpy(previousTimeString, timeString);
    }
  }
}
