import RPi.GPIO as GPIO
import time

# Pin definition
PIN_LED = 18

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_LED, GPIO.OUT)

try:
    print("2-Pin LED Test")
    print("LED should be blinking...")
    print("Press Ctrl+C to exit")
    
    while True:
        print("LED ON")
        GPIO.output(PIN_LED, GPIO.HIGH)  # Turn LED on
        time.sleep(1)
        
        print("LED OFF")
        GPIO.output(PIN_LED, GPIO.LOW)   # Turn LED off
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped")
    
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")