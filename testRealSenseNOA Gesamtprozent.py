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

        # Masken für nahe, mittlere und ferne Bereiche erstellen
        # Tiefenwerte in Millimetern
        near_threshold = 500  # <= 0,5 Meter
        middle_threshold = 2000  # <= 2 Meter
        
        # Zähle Pixel in den Bereichen
        total_pixels = depth_image.size
        near_pixels = np.sum(depth_image <= near_threshold)
        middle_pixels = np.sum((depth_image > near_threshold) & (depth_image <= middle_threshold))
        far_pixels = np.sum(depth_image > middle_threshold)

        # Dominanten Bereich bestimmen
        near_percentage = (near_pixels / total_pixels) * 100
        middle_percentage = (middle_pixels / total_pixels) * 100
        far_percentage = (far_pixels / total_pixels) * 100

        # Berechnung eines Distanzwertes (0-100%)
        # Gewichtung: Nah (1.0), Mittel (0.5), Fern (0.0)
        normalized_value = (
            (near_percentage * 1.0) +
            (middle_percentage * 0.5) +
            (far_percentage * 0.0)
        ) / 100
        percentage_value = normalized_value * 100

        # Ausgabe des berechneten Wertes
        print(f"Distanz-Wert (0-100%): {percentage_value:.2f}%")

        # Tiefenbild anzeigen
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)  # alpha ändert was empfindlichkeit nähe
        cv2.imshow("Depth Image", depth_colormap)


        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()