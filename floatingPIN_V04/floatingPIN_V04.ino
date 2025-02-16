#include <Adafruit_NeoPixel.h>

// *** Einstellungen *** //
#define LED_PIN 4                // Datenpin für die LEDs
#define NUM_LEDS 12              // Anzahl der LEDs
#define FLOAT_PIN A0             // Floating-Pin für analogRead()

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

// *** Farbwerte für Blau, Türkis, Lila *** //
void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.show(); // Alle LEDs ausschalten
}

// *** Variablen für Glättung und Schwellwert *** //
float smoothedValue = 0;        // Gefilterter Wert
const float alpha = 0.4;        // Glättungsfaktor (zwischen 0 und 1)
const uint8_t threshold = 10;       // Minimale Signaländerung
uint8_t lastValue = 0;              // Vorheriger Wert zur Überprüfung von Änderungen

void loop() {
  uint8_t sensorValue = analogRead(FLOAT_PIN);

  // Glättung mit Low-Pass-Filter
  smoothedValue = alpha * sensorValue + (1 - alpha) * smoothedValue;

  Serial.print("smoothedValue: ");
  Serial.println(smoothedValue);

  // Ignoriere minimale Änderungen unterhalb des Schwellwerts
  if (abs((uint8_t)smoothedValue - lastValue) > threshold) {
    lastValue = (uint8_t)smoothedValue;
    updateLEDs((uint8_t)smoothedValue); // Aktualisiere die LEDs mit dem gefilterten Wert
  }

  delay(50); // Kurze Pause für Stabilität
}

void updateLEDs(uint8_t sensorValue) {
  // Normalisiere den Wert auf die Anzahl der LEDs
  uint8_t numActiveLEDs = map(sensorValue, 0, 1023, 0, NUM_LEDS);

  // Bestimme die Intensität des Lichts (Helligkeit)
  uint8_t brightness = map(sensorValue, 0, 1023, 50, 255); // Von schwach bis hell

  // Bestimme die Farbe basierend auf dem Signal
  uint8_t r, g, b;
  if (sensorValue < 341) {
    r = 0; g = 128; b = 255; // Hellblau
  } else if (sensorValue < 682) {
    r = 0; g = 255; b = 255; // Türkis
  } else {
    r = 128; g = 0; b = 255; // Lila
  }

  // LEDs aktualisieren
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    if (i < numActiveLEDs) {
      // Setze Farbe und Helligkeit für aktive LEDs
      strip.setPixelColor(i, strip.Color(r * brightness / 255, g * brightness / 255, b * brightness / 255));
    } else {
      // Deaktiviere restliche LEDs
      strip.setPixelColor(i, 0, 0, 0);
    }
  }

  strip.show();
}