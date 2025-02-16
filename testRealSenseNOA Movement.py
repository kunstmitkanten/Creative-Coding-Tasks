import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
 
pipeline.start(config)

previous_depth = None

try:
    while True:
        # Warten auf ein Frame
        frames = pipeline.wait_for_frames()
        if not frames:
            print("Keine Frames empfangen. Stelle sicher, dass die Kamera angeschlossen ist.")
            continue

        depth_frame = frames.get_depth_frame()
        
        current_depth = np.asanyarray(depth_frame.get_data())

        if previous_depth is not None:
            # Absolute Differenz zwischen aktuellem und vorherigem Frame
            depth_difference = cv2.absdiff(current_depth, previous_depth)

            # Bewegungsschwellenwert (Pixel, die sich mehr als 50 mm geändert haben)
            movement_threshold = 1000  # In Millimetern
            movement_mask = depth_difference > movement_threshold

            # Tiefenbild auf bewegte Bereiche beschränken
            moving_depth = np.where(movement_mask, current_depth, 0)

            # Berechnung der Tiefenstatistik für die bewegten Objekte
            moving_pixels = np.sum(movement_mask)
            if moving_pixels > 0:
                avg_moving_depth = np.sum(moving_depth) / moving_pixels
                print(f"Durchschnittliche Tiefe bewegter Objekte: {avg_moving_depth:.2f} mm")
            else:
                print("Keine Bewegung erkannt.")

            # Visualisierung der Bewegung
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(moving_depth, alpha=0.03), cv2.COLORMAP_JET)
            cv2.imshow("Bewegung (Depth)", depth_colormap)

        # Aktuelles Frame als vorheriges Frame speichern
        previous_depth = current_depth.copy()


        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()