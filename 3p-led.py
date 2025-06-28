#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

PIN_LED = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_LED, GPIO.OUT)

def test_common_anode():
    """Test for common anode bi-color LED"""
    print("Testing Common Anode logic (inverted)...")
    
    print("Setting GPIO HIGH for RED LED (common anode)")
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(2)
    
    print("Setting GPIO LOW for GREEN LED (common anode)")
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(2)

def red_led_anode():
    """RED LED for common anode"""
    GPIO.output(PIN_LED, GPIO.HIGH)

def green_led_anode():
    """GREEN LED for common anode"""
    GPIO.output(PIN_LED, GPIO.LOW)

try:
    print("Testing if module is Common Anode...")
    test_common_anode()
    
    print("If colors were correct above, your module IS common anode")
    print("Continuous test with correct logic:")
    
    while True:
        print("RED")
        red_led_anode()
        time.sleep(1)
        print("GREEN") 
        green_led_anode()
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted")
finally:
    GPIO.cleanup()