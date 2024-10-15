import asyncio
import libcamera
import time
import cv2

async def capture_image():
    # Create a CameraManager
    camera_manager = libcamera.CameraManager()
    await camera_manager.start()
    
    # List available cameras
    cameras = camera_manager.cameras
    if not cameras:
        print("No cameras found!")
        return

    # Select the first camera
    camera = cameras[0]

    # Configure the camera
    configuration = camera.generate_configuration()
    camera.configure(configuration)

    # Start the camera
    await camera.start()
    
    # Allow the camera to warm up
    time.sleep(2)

    # Capture an image
    request = camera.create_request()
    request.capture()
    print("Image captured.")

    # Stop the camera
    await camera.stop()
    await camera_manager.stop()

# Run the capture image function
asyncio.run(capture_image())
