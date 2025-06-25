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

# Initialize PWM at 100 Hz
pwm_led = GPIO.PWM(PIN_LED, 100)

# Start PWM with 0% duty cycle (off)
pwm_led.start(0)

def blink_led(times=5, interval=0.5):
    """Blink the LED a specified number of times"""
    for _ in range(times):
        GPIO.output(PIN_LED, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(PIN_LED, GPIO.LOW)
        time.sleep(interval)

def fade_led(duration=2.0, steps=100):
    """Fade the LED smoothly from off to on and back to off"""
    # Fade up
    for duty in range(0, 101, 1):
        pwm_led.ChangeDutyCycle(duty)
        time.sleep(duration / (2 * steps))
    
    # Fade down
    for duty in range(100, -1, -1):
        pwm_led.ChangeDutyCycle(duty)
        time.sleep(duration / (2 * steps))

try:
    print("Simple Single LED Module Demo")
    print("Press Ctrl+C to exit")
    
    # Simple on/off demo
    print("1. Turning LED on for 2 seconds...")
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(1)
    
    # Blinking demo
    print("2. Blinking LED...")
    blink_led(times=5, interval=0.3)
    time.sleep(1)
    
    # PWM fading demo
    print("3. Fading the LED...")
    fade_led(duration=3.0)
    time.sleep(1)
    
    # Loop through all patterns
    print("4. Continuous demo loop... (Press Ctrl+C to exit)")
    while True:
        blink_led(times=3, interval=0.2)
        time.sleep(0.5)
        fade_led(duration=2.0)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program interrupted by user")
    
finally:
    # Clean up
    pwm_led.stop()
    GPIO.cleanup()
    print("GPIO cleaned up, exiting.")
