from picamera2 import Picamera2
import cv2
import time
import os
from datetime import datetime
<<<<<<< HEAD
import numpy as np
from collections import deque
from threading import Thread
=======
>>>>>>> 16a40be (store video every 5 second)

class Camera:
    def __init__(self,
                 video_directory="/home/peworo/Desktop/Home-security-system/RaspPi/Videos/",
                 resolution=(640, 480),
                 fps=30,
<<<<<<< HEAD
<<<<<<< HEAD
                 segment_duration=5,
                 max_videos=4,
                 critical_duration=7):  # Duration of critical video before and after event trigger
=======
                 segment_duration=10):  # 300 seconds = 5 minutes
>>>>>>> 16a40be (store video every 5 second)
=======
                 segment_duration=20,
                 max_videos=5):  # Store only the latest 10 videos
>>>>>>> fbaf0f4 (Storing certain amount of video and delete the previous ones)
        # Initialize camera
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": resolution, "format": "RGB888"})
        self.picam2.configure(config)
        
        # Video settings
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_directory = video_directory
        self.resolution = resolution
        self.fps = fps
<<<<<<< HEAD
        self.segment_duration = segment_duration
        self.max_videos = max_videos
        self.critical_duration = critical_duration
=======
        self.segment_duration = segment_duration  # Duration of each video segment in seconds
<<<<<<< HEAD
>>>>>>> 16a40be (store video every 5 second)
=======
        self.max_videos = max_videos  # Maximum number of video files to keep
>>>>>>> fbaf0f4 (Storing certain amount of video and delete the previous ones)
        
        # Ensure the video directory exists
        os.makedirs(self.video_directory, exist_ok=True)
        
        # Initialize VideoWriter
        self.output = None
        self.start_time = None
<<<<<<< HEAD
        
        # Buffer for critical video (store past frames)
        self.frame_buffer = deque(maxlen=int(self.fps * self.critical_duration))

        # Flag for critical video recording
        self.is_critical_recording = False
        self.critical_output = None
    
    def _get_new_video_filename(self, prefix="video"):
        """Generate a new video filename with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.video_directory, f"{prefix}_{timestamp}.mp4")
=======
    
    def _get_new_video_filename(self):
        """Generate a new video filename with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.video_directory, f"video_{timestamp}.mp4")
>>>>>>> 16a40be (store video every 5 second)
    
    def start_camera(self):
        """Start the camera stream."""
        self.picam2.start()
        print("Camera started")
        self._start_new_video()
    
    def _start_new_video(self):
        """Start a new video segment."""
        if self.output:
            self.output.release()
            print(f"Saved video segment: {self.current_filename}")
        self.current_filename = self._get_new_video_filename()
        self.output = cv2.VideoWriter(self.current_filename, self.fourcc, self.fps, self.resolution)
        self.start_time = time.time()
        print(f"Started new video segment: {self.current_filename}")
<<<<<<< HEAD
<<<<<<< HEAD
        
        # Manage video storage to keep only the latest videos
        self._manage_video_storage()
    
    def _manage_video_storage(self):
        """Delete the oldest video if the maximum number of non-critical videos is exceeded."""
        # Get a list of all video files, excluding critical videos
        video_files = sorted([
            f for f in os.listdir(self.video_directory)
            if f.endswith(".mp4") and not f.startswith("critical")
        ])
=======
        
        # Manage video storage to keep only the latest 10 videos
        self._manage_video_storage()
    
    def _manage_video_storage(self):
        """Delete the oldest video if the maximum number of videos is exceeded."""
        video_files = sorted([f for f in os.listdir(self.video_directory) if f.endswith(".mp4")])
>>>>>>> fbaf0f4 (Storing certain amount of video and delete the previous ones)
        if len(video_files) > self.max_videos:
            oldest_file = os.path.join(self.video_directory, video_files[0])
            os.remove(oldest_file)
            print(f"Deleted oldest video segment: {oldest_file}")
<<<<<<< HEAD

=======
>>>>>>> 16a40be (store video every 5 second)
=======
>>>>>>> fbaf0f4 (Storing certain amount of video and delete the previous ones)
    
    def capture_frame(self):
        """Capture a single frame and write it to the current video segment."""
        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        correction_matrix = np.array([[0.68, 0, 0], [0, 1, 0], [0, 0, 0.8]])  # Adjust these values
        frame = cv2.transform(frame, correction_matrix)
        
        # Display frame
        cv2.imshow("Pi Camera Feed", frame)
        
        # Write to current video segment
        if self.output:
            self.output.write(frame)
        
<<<<<<< HEAD
        # Buffer the frame for critical video
        self.frame_buffer.append(frame)
        
        # Handle critical video recording if active
        if self.is_critical_recording:
            if self.critical_output:
                self.critical_output.write(frame)
                if time.time() - self.critical_start_time >= self.critical_duration:
                    self._stop_critical_video()
        
=======
>>>>>>> 16a40be (store video every 5 second)
        # Check if the current segment has reached the duration limit
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.segment_duration:
            self._start_new_video()
    
<<<<<<< HEAD
    def start_critical_video(self):
        """Start recording a critical video that includes past frames and continues recording."""
        if not self.is_critical_recording:
            self.is_critical_recording = True
            self.critical_start_time = time.time()
            critical_filename = self._get_new_video_filename(prefix="critical")
            self.critical_output = cv2.VideoWriter(critical_filename, self.fourcc, self.fps, self.resolution)
            
            # Write buffered frames (past frames)
            for buffered_frame in self.frame_buffer:
                self.critical_output.write(buffered_frame)
            print(f"Started critical video recording: {critical_filename}")
    
    def _stop_critical_video(self):
        """Stop recording the critical video and reset flags."""
        if self.critical_output:
            self.critical_output.release()
            print("Critical video saved.")
        self.is_critical_recording = False
        self.critical_output = None
    
=======
>>>>>>> 16a40be (store video every 5 second)
    def stop_camera(self):
        """Stop the camera, release resources, and close all windows."""
        if self.output:
            self.output.release()
            print(f"Saved final video segment: {self.current_filename}")
<<<<<<< HEAD
        if self.is_critical_recording:
            self._stop_critical_video()
=======
>>>>>>> 16a40be (store video every 5 second)
        cv2.destroyAllWindows()
        self.picam2.close()
        print("Camera stopped and resources released")
    
    def record(self):
        """Continuously capture frames and record until 'q' is pressed."""
        self.start_camera()
        try:
            while True:
                self.capture_frame()
<<<<<<< HEAD
                # Press 'c' to trigger critical recording
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    self.start_critical_video()
                # Press 'q' to stop recording
                elif cv2.waitKey(1) & 0xFF == ord('q'):
=======
                # Press 'q' to stop recording
                if cv2.waitKey(1) & 0xFF == ord('q'):
>>>>>>> 16a40be (store video every 5 second)
                    break
        finally:
            self.stop_camera()

if __name__ == "__main__":
    # Define the directory where videos will be saved
    video_directory = "/home/peworo/Desktop/Home-security-system/RaspPi/Videos/"
    
    # Create a Camera object
    camera = Camera(video_directory=video_directory)
    
    # Start recording
    camera.record()