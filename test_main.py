import paho.mqtt.client as mqtt
import time
from Notification.alert import email_alert
import threading
from RaspPi.Camera.store_video import Camera

detected_time = None
last_email_time = 0  # Initialize the last email sent time

myCamera = Camera()
camera_thread = threading.Thread(target=myCamera.record)
camera_thread.start()
print("---- Thread started ----")

# Callback when the client connects to the broker
def on_connect():
    print("Connected!")
    # Subscribe to the topic
    time.sleep(3)

# Callback when a message is received from the broker
def on_message():
    global last_email_time  # Make sure we're modifying the global variable
    data = 0

    initial_time = time.time()
    try:
        while True:
            print("Recieving data.")
            current_time = time.time()
            if current_time - initial_time > 10:
                detected_time = time.time()
                print(f"Alert! {data} > 10!")
                
                if detected_time - last_email_time > 5:
                    last_email_time = detected_time  # Update the last email sent time
                    handle_high_value(data, detected_time)
    except ValueError:
        print("Received non-numeric data")

# Define a function to handle high values
def handle_high_value(data, detected_time):
    # Define your action here when the data goes above the threshold
    print(f"Sending email: {data}")
    # email_alert("Home Security System Alert", "Your home has been invaded!", "sakari.heinio@gmail.com")
    myCamera.commands.put('start_critical_video')


if __name__ == "__main__" :
    on_connect()
    on_message()
