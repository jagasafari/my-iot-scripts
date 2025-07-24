#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

LED_PIN = 17
DIGITAL_PIN = 27

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(DIGITAL_PIN, GPIO.IN)
    print("Simple pulse detector initialized")

def main():
    setup()
    print("Place finger on sensor...")
    print("LED will blink with detected pulses")
    
    try:
        while True:
            # Read digital signal if available
            if GPIO.input(DIGITAL_PIN):
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("♥", end='', flush=True)
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
                print(".", end='', flush=True)
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()