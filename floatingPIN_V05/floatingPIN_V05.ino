#include <Adafruit_NeoPixel.h>

#define FLOAT_PIN 0
#define LED_PIN 4
#define NUM_LEDS 12

Adafruit_NeoPixel ledRing(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

uint8_t lastRead = 0;
uint8_t activeLED = 0;

uint32_t color() {
  uint8_t hue = 0.5;
  uint8_t saturation = 255;
  uint8_t brightness = 120;
  return ledRing.ColorHSV(hue, saturation, brightness);
}

uint32_t lightUpLEDs(uint32_t currentRead) {
  uint32_t section = map(currentRead, 0, 500, 0, 12);
  for (int i = 0; i < 12; i++) {
    if (i < section) {
      ledRing.setPixelColor(i, color());
      ledRing.show();
    } else {
      ledRing.setPixelColor(i, 0);
      ledRing.show();
    }
  }
}

void setup() {
  Serial.begin(9600);
  ledRing.begin();
  ledRing.show();

  pinMode(FLOAT_PIN, INPUT);
}

void loop() {
  delay(500);
  uint8_t currentRead = analogRead(FLOAT_PIN);
  
  Serial.print("SIGNAL: ");
  Serial.println(currentRead);

  lightUpLEDs(currentRead);

}
