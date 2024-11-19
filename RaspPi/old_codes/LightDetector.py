import RPi.GPIO as GPIO
import time

# Define GPIO pin connected to the photoresistor module
ldr_pin = 17  # GPIO 17 (Pin 11)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ldr_pin, GPIO.OUT)
GPIO.output(ldr_pin, GPIO.LOW)
time.sleep(0.1)  # Discharge any capacitance

# Change the pin to input mode to measure time
GPIO.setup(ldr_pin, GPIO.IN)

# Function to measure light intensity based on charge time
def measure_light():
    start_time = time.time()
    
    # Wait for the pin to go from LOW to HIGH
    timeout = time.time() + 5  # 5 seconds timeout
    while GPIO.input(ldr_pin) == GPIO.LOW:
        if time.time() > timeout:
            print("Timeout waiting for light change")
            return None  # Return None if no change after timeout
    
    end_time = time.time()
    
    # Calculate the time difference (charge time)
    charge_time = end_time - start_time
    return charge_time

try:
    while True:
        light_level = measure_light()
        if light_level is not None:
            print("Light level (charge time):", light_level)
        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
