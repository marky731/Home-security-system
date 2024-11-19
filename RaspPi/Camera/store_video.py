import time
import os
from datetime import datetime
import numpy as np
import cv2
from picamera2 import Picamera2
from collections import deque

class Camera:
    def __init__(self,
                 video_directory="videos",
                 resolution=(640, 480),
                 fps=30,
                 segment_duration=15,
                 max_videos=5,
                 critical_buffer_size=5):
        
        # Video settings
        self.video_directory = video_directory
        self.resolution = resolution
        self.fps = fps
        self.segment_duration = segment_duration
        self.max_videos = max_videos
        self.critical_buffer_size = critical_buffer_size
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Initialize Picamera2
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_video_configuration(
            main={"size": resolution, "format": "YUV420"},
            controls={"FrameRate": fps}
        ))

        # Ensure the video directory exists
        os.makedirs(self.video_directory, exist_ok=True)
        
        # Initialize VideoWriter
        self.output_vid_writer = None
        self.start_time = None
        
        # Flag for critical video recording
        self.is_critical_recording = False
        self.critical_frames_buffer = deque(maxlen=2 * critical_buffer_size + 1)
    
    def _get_new_video_filename(self, prefix="video"):
        """Generate a new video filename with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        return os.path.join(self.video_directory, f"{prefix}_{timestamp}.mp4")
    
    def start_camera(self):
        """Start the camera without the Picamera2 preview."""
        self.picam2.start()
        print("Camera started")
        self._start_new_video()
    
    def _start_new_video(self):
        """Start a new video segment."""
        if self.output_vid_writer:
            self.output_vid_writer.release()

        # Start a new segment
        self.current_filename = self._get_new_video_filename()
        self.output_vid_writer = cv2.VideoWriter(self.current_filename, self.fourcc, self.fps, self.resolution)
        self.start_time = time.time()
        print(f"Started new video segment: {self.current_filename}")
        
        # Manage video storage to keep only the latest videos
        self._manage_video_storage()
    
    def _manage_video_storage(self):
        """Delete the oldest video if the maximum number of non-critical videos is exceeded."""
        video_files = sorted([
            f for f in os.listdir(self.video_directory)
            if (f.endswith(".mp4") or f.endswith(".avi")) and not f.startswith("critical")
        ])
        if len(video_files) > self.max_videos:
            oldest_file = os.path.join(self.video_directory, video_files[0])
            os.remove(oldest_file)
            print(f"Deleted oldest video segment: {oldest_file}")
    
    def _save_critical_frames_as_images(self):
        """Save each frame in the buffer as an image file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        for idx, frame in enumerate(self.critical_frames_buffer):
            image_filename = os.path.join(self.video_directory, f"captured_{timestamp}_{idx}.png")
            cv2.imwrite(image_filename, frame)
            print(f"Saved critical frame image: {image_filename}")
    
    def _rename_video_to_critical(self):
        """Rename the current video file to indicate a critical event."""
        critical_filename = self.current_filename.replace("video_", "critical_")
        os.rename(self.current_filename, critical_filename)
        self.current_filename = critical_filename
        print(f"Renamed video to critical: {self.current_filename}")
    
    def capture_frame(self):
        """Capture a single frame and write it to the current video segment."""
        frame = self.picam2.capture_array()

        # Check if the frame is in YUV format and convert to BGR
        if len(frame.shape) == 2 or frame.shape[2] != 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)

        # Apply color correction if needed (ensure frame is 3 channels)
        if frame.shape[2] == 3:
            correction_matrix = np.array([[0.68, 0, 0], [0, 1, 0], [0, 0, 0.8]])  # Adjust values as necessary
            frame = cv2.transform(frame, correction_matrix)

        # Display the frame
        cv2.imshow("Camera Feed", frame)

        # Write to current video segment
        if self.output_vid_writer:
            self.output_vid_writer.write(frame)

        # Buffer the frame for critical capture
        self.critical_frames_buffer.append(frame)

        # Check if the current segment has reached the duration limit
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.segment_duration:
            self._start_new_video()

        # Wait for a short period to control frame rate
        cv2.waitKey(1)

    
    def stop_camera(self):
        """Stop the camera, release resources, and close all windows."""
        if self.output_vid_writer:
            self.output_vid_writer.release()
            print(f"Saved final video segment: {self.current_filename}")
            
        self.picam2.stop()
        cv2.destroyAllWindows()
        print("Camera stopped and resources released")
    
    def record(self):
        """Continuously capture frames and record until 'q' is pressed."""
        self.start_camera()
        try:
            frames_after_critical = 0
            self.is_critical_recording = False
            changed_name_to_critical = False


            while True:
                self.capture_frame()
                time.sleep(0.01)
                
                # Capture key press
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('c') and not changed_name_to_critical:
                    self.is_critical_recording = True

                if self.is_critical_recording and changed_name_to_critical==False:
                    self._rename_video_to_critical()
                    changed_name_to_critical = True
                    frames_after_critical = self.critical_buffer_size
                    print("!!! Critical recording initiated")
                elif self.is_critical_recording:
                    frames_after_critical -= 1
                    if frames_after_critical <= 0:
                        self.is_critical_recording = False
                        self._save_critical_frames_as_images()
                        self.critical_frames_buffer.clear()
                        changed_name_to_critical = False
                elif key == ord('q'):
                    self.stop_camera()
                    print("Stopping camera...")
                    break
        finally:
            self.stop_camera()


if __name__ == "__main__":
    video_directory = "../videos"
    
    camera = Camera(video_directory=video_directory)
    camera.record()
