import paho.mqtt.client as mqtt
import subprocess

THRESHOLD = 1000  # Adjust threshold

# MQTT broker 
BROKER = 'localhost'  
PORT = 1883           
TOPIC = 'sensor/light'  

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic
    client.subscribe(TOPIC)

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        # Assuming the payload is numeric (e.g., light intensity)
        data = float(msg.payload.decode())
        print(f"Received data: {data}")
        # Check if the data goes below the threshold
        if data > THRESHOLD:
            print(f"Alert! Light intensity {data} is above the threshold of {THRESHOLD}!")            
            # React to the condition here, e.g., triggering an alarm or calling another function
            handle_high_value(data)
    except ValueError:
        print("Received non-numeric data")

# Define a function to handle high values
def handle_high_value(data):
    # Define your action here when the data goes below the threshold
    print(f"Taking action for low light intensity: {data}")
    subprocess.run(["python", "alert.py"])

# Create MQTT client
client = mqtt.Client()
# Bind the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)
# Blocking loop to process network traffic and handle callbacks
client.loop_forever()
