#include <lvgl.h>
#include "Arduino_GFX_Library.h"
#include "Arduino_DriveBus_Library.h"
#include "pin_config.h"
#include "lv_conf.h"
#include <Wire.h>
#include <demos/lv_demos.h>
#include "HWCDC.h"
#include "image.h"

HWCDC USBSerial;

#define USB_LOG_ENABLED 0
#if USB_LOG_ENABLED
#define USB_LOG_BEGIN(baud) USBSerial.begin(baud)
#define USB_LOG_PRINT(...) USBSerial.print(__VA_ARGS__)
#define USB_LOG_PRINTLN(...) USBSerial.println(__VA_ARGS__)
#define USB_LOG_PRINTF(...) USBSerial.printf(__VA_ARGS__)
#define USB_LOG_FLUSH() USBSerial.flush()
#else
#define USB_LOG_BEGIN(baud) do {} while (0)
#define USB_LOG_PRINT(...) do {} while (0)
#define USB_LOG_PRINTLN(...) do {} while (0)
#define USB_LOG_PRINTF(...) do {} while (0)
#define USB_LOG_FLUSH() do {} while (0)
#endif
Arduino_DataBus *bus = new Arduino_ESP32SPI(LCD_DC, LCD_CS, LCD_SCK, LCD_MOSI);

Arduino_GFX *gfx = new Arduino_ST7789(bus, LCD_RST /* RST */,
                                      0 /* rotation */, true /* IPS */, LCD_WIDTH, LCD_HEIGHT, 0, 0, 0, 0);


std::shared_ptr<Arduino_IIC_DriveBus> IIC_Bus =
  std::make_shared<Arduino_HWIIC>(IIC_SDA, IIC_SCL, &Wire);

void Arduino_IIC_Touch_Interrupt(void);

std::unique_ptr<Arduino_IIC> CST816T(new Arduino_CST816x(IIC_Bus, CST816T_DEVICE_ADDRESS,
                                                         TP_RST, TP_INT, Arduino_IIC_Touch_Interrupt));

void Arduino_IIC_Touch_Interrupt(void) {
  CST816T->IIC_Interrupt_Flag = true;
}

static const uint32_t TOUCH_HOLD_MS = 80;
static int32_t lastTouchX = 0;
static int32_t lastTouchY = 0;
static uint32_t lastTouchMillis = 0;
static bool lastTouchValid = false;

static bool readTouchPoint(int32_t *x, int32_t *y) {
  if (CST816T->IIC_Interrupt_Flag) {
    CST816T->IIC_Interrupt_Flag = false;
    int32_t touchX = CST816T->IIC_Read_Device_Value(CST816T->Arduino_IIC_Touch::Value_Information::TOUCH_COORDINATE_X);
    int32_t touchY = CST816T->IIC_Read_Device_Value(CST816T->Arduino_IIC_Touch::Value_Information::TOUCH_COORDINATE_Y);

    if (touchX >= 0 && touchX < LCD_WIDTH && touchY >= 0 && touchY < LCD_HEIGHT) {
      lastTouchX = touchX;
      lastTouchY = touchY;
      lastTouchMillis = millis();
      lastTouchValid = true;
    }
  }

  if (!lastTouchValid || millis() - lastTouchMillis > TOUCH_HOLD_MS) {
    lastTouchValid = false;
    return false;
  }

  *x = lastTouchX;
  *y = lastTouchY;
  return true;
}

#define EXAMPLE_LVGL_TICK_PERIOD_MS 2

uint32_t screenWidth;
uint32_t screenHeight;

static lv_disp_draw_buf_t draw_buf;
// static lv_color_t buf[screenWidth * screenHeight / 10];


#if LV_USE_LOG != 0
/* Serial debugging */
void my_print(const char *buf) {
  USB_LOG_PRINT(buf);
  USB_LOG_FLUSH();
}
#endif

/* Display flushing */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p) {
  uint32_t w = (area->x2 - area->x1 + 1);
  uint32_t h = (area->y2 - area->y1 + 1);

#if (LV_COLOR_16_SWAP != 0)
  gfx->draw16bitBeRGBBitmap(area->x1, area->y1, (uint16_t *)&color_p->full, w, h);
#else
  gfx->draw16bitRGBBitmap(area->x1, area->y1, (uint16_t *)&color_p->full, w, h);
#endif

  lv_disp_flush_ready(disp);
}

void example_increase_lvgl_tick(void *arg) {
  /* Tell LVGL how many milliseconds has elapsed */
  lv_tick_inc(EXAMPLE_LVGL_TICK_PERIOD_MS);
}

static uint8_t count = 0;
void example_increase_reboot(void *arg) {
  count++;
  if (count == 30) {
    esp_restart();
  }
}

/*Read the touchpad*/
void my_touchpad_read(lv_indev_drv_t *indev_driver, lv_indev_data_t *data) {
  int32_t touchX = 0;
  int32_t touchY = 0;

  if (readTouchPoint(&touchX, &touchY)) {
    data->state = LV_INDEV_STATE_PR;
    data->point.x = touchX;
    data->point.y = touchY;
  } else {
    data->state = LV_INDEV_STATE_REL;
  }
}


void setup() {
  USB_LOG_BEGIN(115200); /* prepare for possible serial debug */
  Wire.begin(IIC_SDA, IIC_SCL);

  while (CST816T->begin() == false) {
    USB_LOG_PRINTLN("CST816T initialization fail");
    delay(2000);
  }
  USB_LOG_PRINTLN("CST816T initialization successfully");

  CST816T->IIC_Write_Device_State(CST816T->Arduino_IIC_Touch::Device::TOUCH_DEVICE_INTERRUPT_MODE,
                                  CST816T->Arduino_IIC_Touch::Device_Mode::TOUCH_DEVICE_INTERRUPT_PERIODIC);

  gfx->begin();
  pinMode(LCD_BL, OUTPUT);
  digitalWrite(LCD_BL, HIGH);

  screenWidth = gfx->width();
  screenHeight = gfx->height();

  lv_init();

  lv_color_t *buf1 = (lv_color_t *)heap_caps_malloc(screenWidth * screenHeight / 4 * sizeof(lv_color_t), MALLOC_CAP_DMA);

  lv_color_t *buf2 = (lv_color_t *)heap_caps_malloc(screenWidth * screenHeight / 4 * sizeof(lv_color_t), MALLOC_CAP_DMA);

  String LVGL_Arduino = "Hello Arduino! ";
  LVGL_Arduino += String('V') + lv_version_major() + "." + lv_version_minor() + "." + lv_version_patch();

  USB_LOG_PRINTLN(LVGL_Arduino);
  USB_LOG_PRINTLN("I am LVGL_Arduino");



#if LV_USE_LOG != 0
  lv_log_register_print_cb(my_print); /* register print function for debugging */
#endif

  lv_disp_draw_buf_init(&draw_buf, buf1, buf2, screenWidth * screenHeight / 4);

  /*Initialize the display*/
  static lv_disp_drv_t disp_drv;
  lv_disp_drv_init(&disp_drv);
  /*Change the following line to your display resolution*/
  disp_drv.hor_res = screenWidth;
  disp_drv.ver_res = screenHeight;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.draw_buf = &draw_buf;
  lv_disp_drv_register(&disp_drv);

  /*Initialize the (dummy) input device driver*/
  static lv_indev_drv_t indev_drv;
  lv_indev_drv_init(&indev_drv);
  indev_drv.type = LV_INDEV_TYPE_POINTER;
  indev_drv.read_cb = my_touchpad_read;
  lv_indev_drv_register(&indev_drv);

  lv_obj_t *label = lv_label_create(lv_scr_act());
  lv_label_set_text(label, "Hello Ardino and LVGL!");
  lv_obj_align(label, LV_ALIGN_CENTER, 0, 0);

  const esp_timer_create_args_t lvgl_tick_timer_args = {
    .callback = &example_increase_lvgl_tick,
    .name = "lvgl_tick"
  };

  const esp_timer_create_args_t reboot_timer_args = {
    .callback = &example_increase_reboot,
    .name = "reboot"
  };

  esp_timer_handle_t lvgl_tick_timer = NULL;
  esp_timer_create(&lvgl_tick_timer_args, &lvgl_tick_timer);
  esp_timer_start_periodic(lvgl_tick_timer, EXAMPLE_LVGL_TICK_PERIOD_MS * 1000);

  lv_demo_widgets();
  // lv_demo_benchmark();
  // lv_demo_keypad_encoder();
  // lv_demo_music();
  // lv_demo_stress();

  // lv_obj_t *img_obj = lv_img_create(lv_scr_act());
  // lv_img_set_src(img_obj, &img_test3);  // Set the image source to img_test3
  // lv_obj_align(img_obj, LV_ALIGN_CENTER, 0, 0);
  // USB_LOG_PRINTLN("Setup done");
}

void loop() {
  lv_timer_handler(); /* let the GUI do its work */
  delay(5);
}
