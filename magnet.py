#!/usr/bin/env python3
# filepath: /home/user/my-iot-scripts/magnet.py

import RPi.GPIO as GPIO
import time

# Configuration
HALL_SENSOR_PIN = 17  # GPIO pin connected to the digital output (D0) of the sensor

def setup():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HALL_SENSOR_PIN, GPIO.IN)
    print("Simple magnet sensor test initialized")

def main():
    """Main program - continuously read sensor value"""
    try:
        setup()
        print("\n=== Simple Magnet Sensor Test ===")
        print(f"Reading from GPIO pin {HALL_SENSOR_PIN}")
        print("Move a magnet near the sensor to test")
        print("Press Ctrl+C to exit\n")
        print("Current value | Status")
        print("-----------------------")
        while True:
            value = GPIO.input(HALL_SENSOR_PIN)
            if value == 1:
                print(f"\r    HIGH (1)   | {'DETECTED' if value else 'NOT DETECTED'}", end="", flush=True)
            else:
                print(f"\r    LOW (0)    | {'DETECTED' if value else 'NOT DETECTED'}", end="", flush=True)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    finally:
        GPIO.cleanup()
        print("\nGPIO cleanup completed")

if __name__ == "__main__":
    main()