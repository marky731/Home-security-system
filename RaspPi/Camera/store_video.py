from picamera2 import Picamera2
import cv2
import time

class Camera:
    def __init__(self, long_video_location = "/home/peworo/Desktop/Home-security-system/RaspPi/Videos/full_video.mp4", short_video_location = "/home/peworo/Desktop/Home-security-system/RaspPi/Videos/short_video.mp4", resolution=(640, 480), fps=30):
        # Initialize camera
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": resolution, "format": "RGB888"})
        self.picam2.configure(config)
        
        # Video settings
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.long_video_location = long_video_location
        self.short_video_location = short_video_location
        self.resolution = resolution
        self.fps = fps
        self.output_full = cv2.VideoWriter(long_video_location, self.fourcc, fps, resolution)
        self.output_buffer = cv2.VideoWriter(short_video_location, self.fourcc, fps, resolution)
        
        # Buffer for last 5 seconds of frames
        self.frame_buffer = []
        self.buffer_size = fps * 5  # Stores frames for the last 5 seconds at the given FPS

    def start_camera(self):
        """Start the camera stream."""
        self.picam2.start()
        print("Camera started")

    def capture_frame(self):
        """Capture a single frame and add it to the buffer."""
        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Display frame
        cv2.imshow("Pi Camera Feed", frame)
        
        # Write to full video
        self.output_full.write(frame)
        
        # Add frame to buffer, maintaining the last 5 seconds
        self.frame_buffer.append(frame)
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer.pop(0)

    def save_short_video(self):
        """Save the last 5 seconds of frames to the short video file."""
        for frame in self.frame_buffer:
            self.output_buffer.write(frame)
        print("Short video saved")

    def stop_camera(self):
        """Stop the camera, release resources, and close all windows."""
        self.save_short_video()
        self.output_full.release()
        self.output_buffer.release()
        cv2.destroyAllWindows()
        self.picam2.close()
        print("Camera stopped and resources released")

    def record(self):
        """Continuously capture frames and record until 'q' is pressed."""
        self.start_camera()
        while True:
            self.capture_frame()
            # Press 'q' to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.stop_camera()

if __name__ == "__main__":
    long_video_path = "/home/peworo/Desktop/Home-security-system/RaspPi/Videos/full_video.mp4"
    short_video_path = "/home/peworo/Desktop/Home-security-system/RaspPi/Videos/short_video.mp4"
    
    # Create a Camera object
    camera = Camera(long_video_path, short_video_path)
    
    # Start recording
    camera.record()
