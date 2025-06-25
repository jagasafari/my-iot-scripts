#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Pin definitions for the two LED modules
PIN_LED1 = 23  # GPIO pin for first LED module
PIN_LED2 = 24  # GPIO pin for second LED module

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Configure pins as outputs
GPIO.setup(PIN_LED1, GPIO.OUT)
GPIO.setup(PIN_LED2, GPIO.OUT)

# Initialize PWM on both pins at 100 Hz
pwm_led1 = GPIO.PWM(PIN_LED1, 100)
pwm_led2 = GPIO.PWM(PIN_LED2, 100)

# Start PWM with 0% duty cycle (off)
pwm_led1.start(0)
pwm_led2.start(0)

def blink_leds(times=5, interval=0.5):
    """Blink both LEDs a specified number of times"""
    for _ in range(times):
        GPIO.output(PIN_LED1, GPIO.HIGH)
        GPIO.output(PIN_LED2, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(PIN_LED1, GPIO.LOW)
        GPIO.output(PIN_LED2, GPIO.LOW)
        time.sleep(interval)

def alternate_leds(times=10, interval=0.3):
    """Alternate between the two LEDs"""
    for _ in range(times):
        GPIO.output(PIN_LED1, GPIO.HIGH)
        GPIO.output(PIN_LED2, GPIO.LOW)
        time.sleep(interval)
        GPIO.output(PIN_LED1, GPIO.LOW)
        GPIO.output(PIN_LED2, GPIO.HIGH)
        time.sleep(interval)

def fade_led(pwm, duration=2.0, steps=100):
    """Fade an LED smoothly from off to on and back to off"""
    # Fade up
    for duty in range(0, 101, 1):
        pwm.ChangeDutyCycle(duty)
        time.sleep(duration / (2 * steps))
    
    # Fade down
    for duty in range(100, -1, -1):
        pwm.ChangeDutyCycle(duty)
        time.sleep(duration / (2 * steps))

try:
    print("Simple LED Module Demo")
    print("Press Ctrl+C to exit")
    
    # Simple on/off demo
    print("1. Turning both LEDs on for 2 seconds...")
    GPIO.output(PIN_LED1, GPIO.HIGH)
    GPIO.output(PIN_LED2, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(PIN_LED1, GPIO.LOW)
    GPIO.output(PIN_LED2, GPIO.LOW)
    
    # Blinking demo
    print("2. Blinking both LEDs...")
    blink_leds(times=5, interval=0.3)
    
    # Alternating demo
    print("3. Alternating the LEDs...")
    alternate_leds(times=10, interval=0.2)
    
    # PWM fading demo
    print("4. Fading the first LED...")
    fade_led(pwm_led1, duration=3.0)
    
    print("5. Fading the second LED...")
    fade_led(pwm_led2, duration=3.0)
    
    print("6. Fading both LEDs together...")
    for duty in range(0, 101, 1):
        pwm_led1.ChangeDutyCycle(duty)
        pwm_led2.ChangeDutyCycle(duty)
        time.sleep(0.03)
    
    for duty in range(100, -1, -1):
        pwm_led1.ChangeDutyCycle(duty)
        pwm_led2.ChangeDutyCycle(duty)
        time.sleep(0.03)
    
    # Loop through all patterns
    print("7. Continuous demo loop... (Press Ctrl+C to exit)")
    while True:
        blink_leds(times=3, interval=0.2)
        time.sleep(0.5)
        alternate_leds(times=5, interval=0.15)
        time.sleep(0.5)
        fade_led(pwm_led1, duration=2.0)
        fade_led(pwm_led2, duration=2.0)

except KeyboardInterrupt:
    print("Program interrupted by user")
    
finally:
    # Clean up
    pwm_led1.stop()
    pwm_led2.stop()
    GPIO.cleanup()
    print("GPIO cleaned up, exiting.")