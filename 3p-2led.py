#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Pin definition for the bi-color LED module
PIN_LED = 23  # GPIO pin for the signal (S pin)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configure pin as output
GPIO.setup(PIN_LED, GPIO.OUT)

def red_led():
    """Turn on RED LED"""
    GPIO.output(PIN_LED, GPIO.LOW)

def green_led():
    """Turn on GREEN LED"""
    GPIO.output(PIN_LED, GPIO.HIGH)

def test_both_colors():
    """Test both colors"""
    print("Testing RED LED...")
    red_led()
    time.sleep(2)
    
    print("Testing GREEN LED...")
    green_led()
    time.sleep(2)

def blink_alternate(times=5, interval=0.5):
    """Alternate between red and green"""
    for i in range(times):
        print(f"Blink {i+1}: RED")
        red_led()
        time.sleep(interval)
        print(f"Blink {i+1}: GREEN")
        green_led()
        time.sleep(interval)

def traffic_light_demo():
    """Simple traffic light simulation"""
    print("Traffic light demo:")
    print("  RED (Stop)")
    red_led()
    time.sleep(3)
    
    print("  GREEN (Go)")
    green_led()
    time.sleep(3)

try:
    print("Bi-Color LED Module Demo")
    print("This module has RED and GREEN LEDs")
    print("Press Ctrl+C to exit")
    
    # Test both colors
    print("\n1. Testing both colors...")
    test_both_colors()
    time.sleep(1)
    
    # Alternating blink demo
    print("\n2. Alternating blink demo...")
    blink_alternate(times=6, interval=0.3)
    time.sleep(1)
    
    # Traffic light simulation
    print("\n3. Traffic light simulation...")
    traffic_light_demo()
    time.sleep(1)
    
    # Continuous alternating loop
    print("\n4. Continuous alternating... (Press Ctrl+C to exit)")
    while True:
        red_led()
        time.sleep(0.5)
        green_led()
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nProgram interrupted by user")
    
finally:
    GPIO.cleanup()
    print("GPIO cleaned up, exiting.")