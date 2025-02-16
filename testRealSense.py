import pip
import pyrealsense2 as rs
import numpy as np
import cv2

# Setup für RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth)  # Tiefenstream aktivieren

# Pipeline starten
pipeline.start(config)

try:
    while True:
        # Warten auf ein Frame
        frames = pipeline.wait_for_frames()

        # Holen des Tiefenbildes
        depth_frame = frames.get_depth_frame()
        
        # Wenn es kein Tiefenbild gibt, überspringen
        if not depth_frame:
            continue
        
        # Konvertiere Tiefenbild zu numpy Array
        depth_image = np.asanyarray(depth_frame.get_data())

        # Anzeigen des Tiefenbildes (optional)
        cv2.imshow('Depth Image', depth_image)

        # Beispiel: Berechne den Abstand an einer Position (x=320, y=240)
        x, y = 320, 240  # Zentrum des Bildes
        depth = depth_frame.get_distance(x, y)  # Abstand an der Pixelposition
        print(f"Abstand an Position ({x}, {y}): {depth} Meter")

        # Wenn Escape gedrückt wird, breche ab
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()