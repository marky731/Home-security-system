import paho.mqtt.client as mqtt
import time
from Notification.alert import email_alert
import threading
from Camera.store_video import Camera

THRESHOLD = 3100  # Adjust threshold

# MQTT broker
BROKER = 'localhost'
PORT = 1883
TOPIC = 'sensor/light'

detected_time = None
last_email_time = 0  # Initialize the last email sent time

myCamera = Camera()
camera_thread = threading.Thread(target=myCamera.record)
camera_thread.start()
print("---- Thread started ----")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic
    client.subscribe(TOPIC)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    global last_email_time  # Make sure we're modifying the global variable
    try:
        # Assuming the payload is numeric (e.g., light intensity)
        data = float(msg.payload.decode())
        print(f"Received data: {data}")
        # Check if the data is above the threshold
        if data > THRESHOLD:
            detected_time = time.time()
            print(f"Alert! {data} > {THRESHOLD}!")
            
            # Only send email if 5 seconds have passed since the last one
            if detected_time - last_email_time > 15:
                last_email_time = detected_time  # Update the last email sent time
                handle_high_value(data, detected_time)
    except ValueError:
        print("Received non-numeric data")

# Define a function to handle high values
def handle_high_value(data, detected_time):
    # Define your action here when the data goes above the threshold
    print(f"!!!Sending email: {data}")
    myCamera.is_critical_recording = True
    email_alert("Home Security System Alert", "Your home has been invaded!", "ikramuyghur24@gmail.com")

# Create MQTT client
client = mqtt.Client()
# Bind the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)
# Blocking loop to process network traffic and handle callbacks
client.loop_forever()

