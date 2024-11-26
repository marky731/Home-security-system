from serial import Serial

import time

# Open the serial port (replace with your correct port)
ser = Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)  # Wait for the connection to establish


try:
    while True:
        if ser.in_waiting > 0:
            # Read and decode the line from the serial port
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    ser.close()  # Close the serial port when done
