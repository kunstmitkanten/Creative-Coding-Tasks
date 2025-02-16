import pyrealsense2 as rs
import numpy as np
import cv2

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

        # Pixelanteile berechnen
        total_pixels = depth_colormap.size / 3  # Gesamtanzahl der Pixel
        blue_percentage = (np.sum(blue_mask > 0) / total_pixels) * 100
        #red_percentage = (np.sum(red_mask > 0) / total_pixels) * 100
        #yellow_percentage = (np.sum(yellow_mask > 0) / total_pixels) * 100

        #normalized_value = (
        #    (blue_percentage * 1.0) +  # Blau -> Gewichtung 1.0
        #    (yellow_percentage * 0.4) +  # Mittel -> Gewichtung 0.5
        #    (red_percentage * 0.0)  # Rot -> Gewichtung 0.0 	
        #) / 100  # Ergebnis auf Bereich 0 bis 1 normieren

        # Optional: Prozentwert (0 bis 100%)
        #percentage_value = normalized_value * 100

        # Ausgabe des Wertes
        print(f"Blau Prozent Wert (0-100%): {blue_percentage:.2f}%")

        #if blue_percentage > 30:
        #    print("Mehr als 50% des Bildes sind nah (Blau).")
        #elif red_percentage > 50:
        #    print("Mehr als 50% des Bildes sind fern (Rot).")
        #elif yellow_percentage > 50:
        #    print("Mehr als 50% des Bildes sind in mittlerer Entfernung (Gelb).")
        #else:
        #    print("Kein dominanter Bereich erkannt.")

        cv2.imshow("Depth Colormap", depth_colormap)
        cv2.imshow("Blue Mask (Nah)", blue_mask)
        #cv2.imshow("Yellow Mask (Mittel)", yellow_mask)
        #cv2.imshow("Red Mask (Fern)", red_mask)

        if cv2.waitKey(1) & 0xFF == 27:
            break

if 30 < blue_percentage < 80:
    

finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()