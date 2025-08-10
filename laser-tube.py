#!/usr/bin/env python3
"""
Laser Module Test Script for Raspberry Pi
Tests a KY-008 laser module connected to GPIO
"""

import RPi.GPIO as GPIO
import time

# GPIO pin configuration
LASER_PIN = 17  # GPIO17 (Pin 11 on Raspberry Pi)

def setup():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LASER_PIN, GPIO.OUT)
    GPIO.output(LASER_PIN, GPIO.LOW)
    print("Laser module initialized on GPIO{}".format(LASER_PIN))

def laser_on():
    """Turn the laser on"""
    GPIO.output(LASER_PIN, GPIO.HIGH)
    print("Laser ON")

def laser_off():
    """Turn the laser off"""
    GPIO.output(LASER_PIN, GPIO.LOW)
    print("Laser OFF")

def blink_laser(times=5, delay=0.5):
    """Blink the laser a specified number of times"""
    print("Blinking laser {} times...".format(times))
    for i in range(times):
        laser_on()
        time.sleep(delay)
        laser_off()
        time.sleep(delay)

def pulse_laser(duration=5):
    """Create a pulsing effect with the laser"""
    print("Pulsing laser for {} seconds...".format(duration))
    start_time = time.time()
    while (time.time() - start_time) < duration:
        for brightness in range(0, 101, 5):
            GPIO.output(LASER_PIN, GPIO.HIGH)
            time.sleep(0.001 * (brightness / 100))
            GPIO.output(LASER_PIN, GPIO.LOW)
            time.sleep(0.001 * (1 - brightness / 100))

def main():
    """Main test routine"""
    try:
        setup()
        
        print("\n=== Laser Module Test ===")
        print("1. Testing basic ON/OFF...")
        laser_on()
        time.sleep(2)
        laser_off()
        time.sleep(1)
        
        print("\n2. Testing blink pattern...")
        blink_laser(times=10, delay=0.2)
        time.sleep(1)
        
        print("\n3. Testing pulse effect...")
        pulse_laser(duration=3)
        
        print("\n4. Interactive mode - Press Enter to toggle, 'q' to quit")
        laser_state = False
        while True:
            user_input = input("Toggle laser (Enter) or quit (q): ")
            if user_input.lower() == 'q':
                break
            laser_state = not laser_state
            if laser_state:
                laser_on()
            else:
                laser_off()
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    finally:
        laser_off()
        GPIO.cleanup()
        print("GPIO cleaned up. Test completed.")

if __name__ == "__main__":
    main()