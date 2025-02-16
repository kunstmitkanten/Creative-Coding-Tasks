#include <Adafruit_NeoPixel.h>

#define FLOAT_PIN 0
#define LED_PIN 4          //mehrere Ringe anschließen oder/und in Reihe
#define NUM_LEDS 12        //??jeweils definieren?

Adafruit_NeoPixel ledRing(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);


uint32_t color() {
  uint8_t hue = random(170, 320); 
  uint8_t saturation = 255;
  uint8_t brightness = 80;
  return ledRing.ColorHSV(hue * 65536L /360, saturation, brightness);
}

void setup() {
  Serial.begin(9600);
  ledRing.begin();
  ledRing.show();

  pinMode(FLOAT_PIN, INPUT);
}

void loop() {
  uint32_t currentRead = analogRead(FLOAT_PIN); //Wert zwischen 0 und 1023
  //Idee: gelesenen Wert durch Anzahl der LEDs teilen und entsprechend Licht verteilen

  switch (currentRead){
    case 15 ... 96 : 
      Serial.println("SIGNAL Stufe 1");
      ledRing.setPixelColor(0, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(0, 0);
    case 97 ... 180 :
      Serial.println("SIGNAL Stufe 2");
      ledRing.setPixelColor(1, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(1, 0);
    case 181 ... 264 :
      Serial.println("SIGNAL Stufe 3");
      ledRing.setPixelColor(2, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(2, 0);
    case 265 ... 348:
      Serial.println("SIGNAL Stufe 4");
      ledRing.setPixelColor(3, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(3, 0);
    case 349 ... 432:
      Serial.println("SIGNAL Stufe 5");
      ledRing.setPixelColor(4, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(4, 0);
    case 433 ... 516:
      Serial.println("SIGNAL Stufe 6");
      ledRing.setPixelColor(5, color());
      ledRing.show();
      delay(50);
      ledRing.setPixelColor(5, 0);
    case 517 ... 600:
      Serial.println("SIGNAL Stufe 7");
      ledRing.setPixelColor(6, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(6, 0);
    case 601 ... 684:
      Serial.println("SIGNAL Stufe 8");
      ledRing.setPixelColor(7, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(7, 0);
    case 685 ... 768:
      Serial.println("SIGNAL Stufe 9");
      ledRing.setPixelColor(8, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(8, 0);
    case 769 ... 852:
      Serial.println("SIGNAL Stufe 10");
      ledRing.setPixelColor(9, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(9, 0);
    case 853 ... 936:
      Serial.println("SIGNAL Stufe 11");
      ledRing.setPixelColor(10, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(10, 0);
    case 937 ... 1024:
      Serial.println("SIGNAL Stufe 12");
      ledRing.setPixelColor(11, color());
      ledRing.show();
      delay(100);
      ledRing.setPixelColor(11, 0);
  }
  
  }
