#include <Adafruit_NeoPixel.h>

#define FLOAT_PIN 0
#define LED_PIN 4
#define NUM_LEDS 12

Adafruit_NeoPixel ledRing(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

uint8_t lastRead = 0;
uint8_t activeLED = 0;

uint32_t color() {
  uint8_t hue = "40E0D0";
  uint8_t saturation = 255;
  uint8_t brightness = 100;
  return ledRing.ColorHSV(hue, saturation, brightness);
}


void setup() {
  Serial.begin(9600);
  ledRing.begin();
  ledRing.show();

  pinMode(FLOAT_PIN, INPUT);

  randomSeed(analogRead(0)); 
}

void loop() {
  uint8_t currentRead = analogRead(FLOAT_PIN);


  if (abs(currentRead - lastRead) >50){           //wenn änderung von letzter lesung zu aktuelle größer als 50
    lastRead = currentRead;
    Serial.print("SIGNAL: ");
    Serial.println(currentRead);

    uint8_t ledON = random(NUM_LEDS);

    for (uint8_t i =0; i <NUM_LEDS; i++){
      if (i == ledON){
        ledRing.setPixelColor(i, color());
      }else{
        ledRing.setPixelColor(i, 0);
      }
    }
    ledRing.show();
  }
delay(1000);
}
