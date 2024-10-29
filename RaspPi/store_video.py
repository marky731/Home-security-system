from picamera2 import Picamera2
import cv2
import numpy as np
import time

# Initialize camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)

# Start the camera
picam2.start()

# Video writer for entire video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 format
output_full = cv2.VideoWriter('full_video.mp4', fourcc, 30.0, (640, 480))

# Video writer for last 5 seconds
output_buffer = cv2.VideoWriter('last_5_seconds.mp4', fourcc, 30.0, (640, 480))

# Variables for last 5 seconds storage
frame_buffer = []  # Circular buffer for frames
buffer_size = 150  # 30 fps * 5 seconds

current_buffer_size = 0

while True:
    # Capture the frame
    frame = picam2.capture_array()

    # Convert frame from RGB to BGR for OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Display the frame using OpenCV
    cv2.imshow("Pi Camera Feed", frame)

    # Write to the full video file
    output_full.write(frame)

    # Add frame to buffer and keep only the last 5 seconds of frames
    frame_buffer.append(frame)
    current_buffer_size += 1 
    if len(frame_buffer) > buffer_size:
        frame_buffer.pop(0)
        current_buffer_size += 1

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Write buffer frames to the last 5 seconds video file
for frame in frame_buffer:
    output_buffer.write(frame)

# Release resources
output_full.release()
output_buffer.release()
cv2.destroyAllWindows()
picam2.close()
