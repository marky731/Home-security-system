from picamera2 import Picamera2
import cv2
import time
import os
from datetime import datetime
import numpy as np
from collections import deque
import threading
import firebase_admin
from firebase_admin import credentials, storage, db

# key for firebase(cloud) adress
cred = credentials.Certificate('/home/peworo/Downloads/homesecurity-c8d2c-firebase-adminsdk-lnqdw-9a879c8769.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'homesecurity-c8d2c.appspot.com',
    'databaseURL': 'https://homesecurity-c8d2c-default-rtdb.firebaseio.com'
})
bucket = storage.bucket()

# uploading video to cloud function
def upload_to_firebase(file_path):
    try:
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        blob.make_public()
        video_url = blob.public_url

    
        ref = db.reference('videos')
        new_video_ref = ref.push()
        new_video_ref.set({
            'url': video_url,
            'description': 'Raspberry Pi video upload'
        })

        print(f"Video uploaded to Firebase Storage and URL saved to Realtime Database: {video_url}")

    except Exception as e:
        print("Failed to upload video to Firebase:", e)

class Camera:
    def __init__(self,
                 video_directory="/home/peworo/Desktop/Home-security-system/RaspPi/Videos/",
                 resolution=(640, 480),
                 fps=30,
                 segment_duration=15,
                 max_videos=5,
                 critical_duration=20):  # Duration of critical video before and after event trigger
        # Initialize camera
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": resolution, "format": "RGB888"})
        self.picam2.configure(config)
        
        # Video settings
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_directory = video_directory
        self.resolution = resolution
        self.fps = fps
        self.segment_duration = segment_duration
        self.max_videos = max_videos
        self.critical_duration = critical_duration
        
        # Ensure the video directory exists
        os.makedirs(self.video_directory, exist_ok=True)
        
        # Initialize VideoWriter
        self.output = None
        self.start_time = None
        
        # Buffer for critical video (store past frames)
        self.frame_buffer = deque(maxlen=int(self.fps * self.critical_duration*2))

        # Flag for critical video recording
        self.is_critical_recording = False
        self.critical_output = None
    
    def _get_new_video_filename(self, prefix="video"):
        """Generate a new video filename with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        return os.path.join(self.video_directory, f"{prefix}_{timestamp}.mp4")
    
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
        
        # Manage video storage to keep only the latest videos
        self._manage_video_storage()
    
    def _manage_video_storage(self):
        """Delete the oldest video if the maximum number of non-critical videos is exceeded."""
        video_files = sorted([
            f for f in os.listdir(self.video_directory)
            if f.endswith(".mp4") and not f.startswith("critical")
        ])
        if len(video_files) > self.max_videos:
            oldest_file = os.path.join(self.video_directory, video_files[0])
            os.remove(oldest_file)
            print(f"Deleted oldest video segment: {oldest_file}")

    
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
        
        # Buffer the frame for critical video
        self.frame_buffer.append(frame)
        
        # Handle critical video recording if active
        if self.is_critical_recording:
            if self.critical_output:
                self.critical_output.write(frame)
                if time.time() - self.critical_start_time >= self.critical_duration:
                    self._stop_critical_video()
        
        # Check if the current segment has reached the duration limit
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.segment_duration:
            self._start_new_video()
    
    def start_critical_video(self):
        """Start recording a critical video that includes past frames and continues recording."""
        if not self.is_critical_recording:
            self.is_critical_recording = True
            self.critical_start_time = time.time()
            critical_filename = self._get_new_video_filename(prefix="critical")
            self.critical_output = cv2.VideoWriter(critical_filename, self.fourcc, self.fps, self.resolution)

            # Start a thread to write buffered frames
            threading.Thread(target=self._write_buffered_frames).start()
            print(f"Started critical video recording: {critical_filename}")

            #upload critical video to cloud
            upload_to_firebase(critical_filename)

    def _write_buffered_frames(self):
        """Write buffered frames (past frames) for the critical video in a separate thread."""
        # Write all buffered frames to the critical output
        while self.frame_buffer:
            buffered_frame = self.frame_buffer.popleft()  # Get and remove the oldest frame
            if self.critical_output:
                self.critical_output.write(buffered_frame)
        print("Buffered frames written to critical video.")
    
    def _stop_critical_video(self):
        """Stop recording the critical video and reset flags."""
        if self.critical_output:
            self.critical_output.release()
            print("Critical video saved.")
        self.is_critical_recording = False
        self.critical_output = None
    
    def stop_camera(self):
        """Stop the camera, release resources, and close all windows."""
        if self.output:
            self.output.release()
            print(f"Saved final video segment: {self.current_filename}")
        if self.is_critical_recording:
            self._stop_critical_video()
        cv2.destroyAllWindows()
        self.picam2.close()
        print("Camera stopped and resources released")
    
    def record(self):
        """Continuously capture frames and record until 'q' is pressed."""
        self.start_camera()
        try:
            while True:
                self.capture_frame()
                # Press 'c' to trigger critical recording
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    self.start_critical_video()
                # Press 'q' to stop recording
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            self.stop_camera()

if __name__ == "__main__":
    video_directory = "/home/peworo/Desktop/Home-security-system/RaspPi/Videos/"
    
    camera = Camera(video_directory=video_directory)
    
    camera.record()