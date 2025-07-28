#!/usr/bin/env python3

# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO pin for flame sensor
FLAME_PIN = 17

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set flame pin as input
GPIO.setup(FLAME_PIN, GPIO.IN)

# Print instructions
print("Flame Detector Test")
print("Be careful with open flames!")
print("Light a match or lighter near sensor")
print("Press Ctrl+C to exit")

try:
  # Main loop
  while True:
    # Read sensor value
    flame = GPIO.input(FLAME_PIN)
    # Print status
    if flame == 0:
      # Print flame detected
      print(
        "\rFLAME DETECTED!", 
        end="", flush=True
      )
    else:
      # Print no flame detected
      print(
        "\rNo flame detected    ", 
        end="", flush=True
      )
    # Wait 0.1 seconds
    time.sleep(0.1)

except KeyboardInterrupt:
  # Handle Ctrl+C
  print("\nStopping...")

finally:
    GPIO.cleanup()