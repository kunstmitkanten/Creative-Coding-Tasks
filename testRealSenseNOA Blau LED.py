import pyrealsense2 as rs
import numpy as np
import cv2
import board
import neopixel
import random
import time


# auf Rasberri: sudo pip install rpi_ws281x adafruit-circuitpython-neopixel

# Kofiguration Intel RealSense
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
 
pipeline.start(config)

# Konfiguration des NeoPixel-Streifens
LED_NUMBER = 60      # Anzahl der LEDs im Strip
LED_PIN = board.D18 # GPIO-Pin (z. B. D18 für Raspberry Pi)
BRIGHTNESS = 0.5    # Helligkeit (zwischen 0.0 und 1.0)

# Initialisierung des NeoPixel-Streifens
pixels = neopixel.NeoPixel(LED_PIN, LED_NUMBER, brightness=BRIGHTNESS, auto_write=False)

# Funktion, um den LED-Streifen zu aktualisieren
def set_led_color(start, end, color):
    for i in range(start, end):
        pixels[i] = color
    pixels.show()

def map_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

def flicker_effect(maxLED):
    # Helligkeitswerte für jede LED speichern
    brightness_values = [random.uniform(0.2, 1.0) for _ in range(maxLED)]  # Startwerte
    
    while True:
        for i in range(maxLED):
            # Sanft die Zielhelligkeit zufällig anpassen
            target_brightness = random.uniform(0.2, 1.0)  # Zufälliger Zielwert
            current_brightness = brightness_values[i]

            # Glatte Überblendung
            new_brightness = current_brightness + (target_brightness - current_brightness) * 0.1
            brightness_values[i] = new_brightness

            # Berechne Farbe basierend auf der Helligkeit (hellblau-weiß)
            flicker_color = (
                int(135 * new_brightness),  # Blau
                int(206 * new_brightness),  # Cyan/Weißlich
                int(250 * new_brightness)   # Weiß
            )
            pixels[i] = flicker_color

        # LEDs aktualisieren
        pixels.show()

        # Kurze Pause, damit das Flackern nicht hektisch wird
        time.sleep(0.05)

try:
    while True:
        # Warten auf ein Frame
        frames = pipeline.wait_for_frames()
        if not frames:
            print("Keine Frames empfangen. Stelle sicher, dass die Kamera angeschlossen ist.")
            continue

        depth_frame = frames.get_depth_frame()
        
        depth_image = np.asanyarray(depth_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)

        # Farbgrenzen für nahe, mittlere und ferne Bereiche
        # Nah (Blau)
        lower_blue = np.array([128, 0, 0])  # Untere Grenze
        upper_blue = np.array([255, 255, 128])  # Obere Grenze 
        blue_mask = cv2.inRange(depth_colormap, lower_blue, upper_blue)

        # Fern (Rot)
        lower_red = np.array([0, 128, 255])  # Untere Grenze
        upper_red = np.array([128, 0, 255])  # Obere Grenze
        red_mask = cv2.inRange(depth_colormap, lower_red, upper_red)

        # Mittlere Distanz (Gelb)
        lower_yellow = np.array([0, 128, 128])  # Untere Grenze
        upper_yellow = np.array([128, 255, 128])  # Obere Grenze
        yellow_mask = cv2.inRange(depth_colormap, lower_yellow, upper_yellow)

        # Nah Pixelanteil berechnen
        total_pixels = depth_colormap.size / 3  # Gesamtanzahl der Pixel
        blue_percentage = (np.sum(blue_mask > 0) / total_pixels) * 100

        # Ausgabe des Wertes
        print(f"Blau Prozent Wert (0-100%): {blue_percentage:.2f}%")

        cv2.imshow("Depth Colormap", depth_colormap)
        cv2.imshow("Blue Mask (Nah)", blue_mask)
       
        if cv2.waitKey(1) & 0xFF == 27:
            break

        # Blauen Anteil auf LED Strip mappen

        maxLEDon = map_range(blue_percentage, 0, 100, 0, LED_NUMBER)
        print(maxLEDon)

        # Aktiviert alle LEDs bis maxLEDon in einer Farbe
        set_led_color(0, LED_NUMBER, (0, 0, 255))

        # Aktiviert flicker effekt für LEDs entsprechend des Blau Anteils
        flicker_effect(maxLEDon)

except KeyboardInterrupt:
    # LEDs ausschalten bei Programmende
    pixels.fill((0, 0, 0))
    pixels.show()

finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()

