import RPi.GPIO as GPIO
import time

# Set up GPIO pin for Hall sensor digital output
hall_pin = 27  # Use GPIO 27 (Pin 13)

# Set up GPIO mode and pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(hall_pin, GPIO.IN)

try:
    while True:
        if GPIO.input(hall_pin) == GPIO.HIGH:
            print("Magnetic field detected!")
        else:
            print("No magnetic field")
        time.sleep(0.5)  # Delay between checks

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on exit
