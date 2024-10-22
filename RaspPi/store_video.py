from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)  # Set the resolution
picam2.preview_configuration.main.format = "XBGR8888"  # Set the format

# Start the camera
picam2.start()

# Video writer for entire video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
output_full = cv2.VideoWriter('full_video.mp4', fourcc, 30.0, (640, 480))

# Variables for last 5 seconds storage
frame_buffer = []  # Circular buffer for frames
buffer_size = 150  # 30 fps * 5 seconds

while True:
    # Capture the frame
    frame = picam2.capture_array()

    # Convert frame from XBGR to BGR

    # Display the frame using OpenCV
    cv2.imshow("Pi Camera Feed", frame)

    # Write to the full video file
    output_full.write(frame)

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
output_full.release()
cv2.destroyAllWindows()
picam2.close()
