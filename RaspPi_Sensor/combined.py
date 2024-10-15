import RPi.GPIO as GPIO
import time

# Define GPIO pins
ldr_pin = 17  # Photoresistor connected to GPIO 17
hall_pin = 27  # Hall sensor digital output connected to GPIO 27

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ldr_pin, GPIO.IN)  # Set LDR pin as input
GPIO.setup(hall_pin, GPIO.IN)  # Set Hall sensor pin as input

try:
    while True:
        # Read light level from photoresistor
        light_level = GPIO.input(ldr_pin)  # Read digital value (0 or 1)

        # Read Hall sensor
        if GPIO.input(hall_pin) == GPIO.HIGH:
            magnetic_field = "Magnetic field detected!"
        else:
            magnetic_field = "No magnetic field"

        # Print readings
        print(f"Light level: {'Dark' if light_level == GPIO.LOW else 'Bright'} | {magnetic_field}")
        time.sleep(1)  # Delay between readings

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
