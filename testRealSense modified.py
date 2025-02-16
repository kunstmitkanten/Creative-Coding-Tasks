import pip

import pyrealsense2 as rs
import numpy as np
import cv2

# Setup für RealSense
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Pipeline starten
pipeline.start(config)

try:

# Initialisierung von vorherigem Frame für Bewegungserkennung
    prev_depth_image = None

    while True:
        # Warten auf ein Frame
        frames = pipeline.wait_for_frames()

        # Holen des Tiefen- und Farbbildes
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        
        # Wenn es kein Tiefenbild gibt, überspringen
        if not depth_frame:
            continue
        
        # Konvertiere Tiefenbild zu numpy Array
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

# Bewegungserkennung: Differenz zwischen aufeinanderfolgenden Frames
        if prev_depth_image is not None:
            diff = cv2.absdiff(cv2.convertScaleAbs(prev_depth_image, alpha=0.03),
                               cv2.convertScaleAbs(depth_image, alpha=0.03))
            _, motion_mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

            # Maske anwenden, um Tiefenwerte des bewegten Objekts zu extrahieren
            motion_mask = motion_mask.astype(bool)
            moving_depth_values = depth_image[motion_mask]

            # Tiefenwerte filtern (z. B. Bereich zwischen 0.5m und 3m)
            valid_depths = moving_depth_values[
                (moving_depth_values > 0.5) & (moving_depth_values < 3.0)
            ]

            if len(valid_depths) > 0:
                # Durchschnittliche Entfernung des bewegten Objekts berechnen
                avg_distance = np.mean(valid_depths)
                print(f"Bewegendes Objekt in ca. {avg_distance:.2f}m Entfernung erkannt")

        # Zeige farbkodiertes Tiefenbild und Bewegung
        cv2.imshow("Color Image", color_image)
        cv2.imshow("Depth Colormap", depth_colormap)
        if prev_depth_image is not None:
            cv2.imshow("Motion Mask", motion_mask.astype(np.uint8) * 255)

        # Update vorheriges Bild
        prev_depth_image = depth_image.copy()

        # Anzeigen des Tiefenbildes (optional)
        cv2.imshow('Depth Image', depth_image)

        # Beispiel: Berechne den Abstand an einer Position (x=320, y=240)
        x, y = 320, 240  # Zentrum des Bildes
        depth = depth_frame.get_distance(x, y)  # Abstand an der Pixelposition
        print(f"Abstand an Position ({x}, {y}): {depth} Meter")

        # Wenn Escape gedrückt wird, breche ab
        #if cv2.waitKey(1) & 0xFF == 27:
        #    break

finally:
    # Stoppe den Stream
    pipeline.stop()
    cv2.destroyAllWindows()