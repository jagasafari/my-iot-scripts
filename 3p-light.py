#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Pin definition for the LED module
PIN_LED = 23  # GPIO pin for the LED module

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configure pin as output
GPIO.setup(PIN_LED, GPIO.OUT)

# Initialize PWM at higher frequency for smoother operation
# Increased from 100Hz to 1000Hz for better LED performance
pwm_led = GPIO.PWM(PIN_LED, 1000)

# Start PWM with 0% duty cycle (off)
pwm_led.start(0)

def test_led_brightness():
    """Test LED at different brightness levels"""
    print("Testing LED brightness levels...")
    
    # Test at 25% brightness
    print("  - 25% brightness")
    pwm_led.ChangeDutyCycle(25)
    time.sleep(2)
    
    # Test at 50% brightness
    print("  - 50% brightness")
    pwm_led.ChangeDutyCycle(50)
    time.sleep(2)
    
    # Test at 75% brightness
    print("  - 75% brightness")
    pwm_led.ChangeDutyCycle(75)
    time.sleep(2)
    
    # Test at 100% brightness
    print("  - 100% brightness")
    pwm_led.ChangeDutyCycle(100)
    time.sleep(2)
    
    # Turn off
    pwm_led.ChangeDutyCycle(0)

def blink_led(times=5, interval=0.5, brightness=100):
    """Blink the LED a specified number of times with adjustable brightness"""
    for _ in range(times):
        pwm_led.ChangeDutyCycle(brightness)
        time.sleep(interval)
        pwm_led.ChangeDutyCycle(0)
        time.sleep(interval)

def fade_led(duration=2.0, steps=100, max_brightness=100):
    """Fade the LED smoothly from off to max brightness and back to off"""
    step_delay = duration / (2 * steps)
    
    # Fade up
    for i in range(steps + 1):
        duty = int((i / steps) * max_brightness)
        pwm_led.ChangeDutyCycle(duty)
        time.sleep(step_delay)
    
    # Fade down
    for i in range(steps, -1, -1):
        duty = int((i / steps) * max_brightness)
        pwm_led.ChangeDutyCycle(duty)
        time.sleep(step_delay)

try:
    print("Enhanced Single LED Module Demo")
    print("Press Ctrl+C to exit")
    
    # Test brightness levels first
    print("1. Testing LED brightness levels...")
    test_led_brightness()
    time.sleep(1)
    
    # Simple on/off demo at full brightness
    print("2. Full brightness test for 3 seconds...")
    pwm_led.ChangeDutyCycle(100)
    time.sleep(3)
    pwm_led.ChangeDutyCycle(0)
    time.sleep(1)
    
    # Blinking demo with full brightness
    print("3. Blinking LED at full brightness...")
    blink_led(times=5, interval=0.3, brightness=100)
    time.sleep(1)
    
    # PWM fading demo
    print("4. Fading the LED...")
    fade_led(duration=3.0, max_brightness=100)
    time.sleep(1)
    
    # Loop through all patterns
    print("5. Continuous demo loop... (Press Ctrl+C to exit)")
    while True:
        blink_led(times=3, interval=0.2, brightness=100)
        time.sleep(0.5)
        fade_led(duration=2.0, max_brightness=100)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program interrupted by user")
    
finally:
    # Clean up
    pwm_led.stop()
    GPIO.cleanup()
    print("GPIO cleaned up, exiting.")
