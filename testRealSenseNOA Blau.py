import pyrealsense2 as rs
import numpy as np
import cv2
import board
import neopixel

# auf Rasberri: sudo pip install rpi_ws281x adafruit-circuitpython-neopixel

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
 
pipeline.start(config)

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



finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()



# timer funktion die in kleinen zeitabständen immer wieder aufgerufen wird und eine 
# eine random helligkeit auswählt in die smooth übergegangen wird 

