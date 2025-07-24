#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    print("Active buzzer test - Press Ctrl+C to exit")
    while True:
        print("Beep!")
        # Turn on
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.5)
        
        print("Silent")
        # Turn off
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    GPIO.cleanup()