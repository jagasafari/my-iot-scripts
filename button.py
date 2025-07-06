import RPi.GPIO as GPIO
import time

# Define constants
PIN_BUTTON = 18  # GPIO pin for button

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Simple button test - one message per press")
    print("Press Ctrl+C to exit")
    
    while True:
        if GPIO.input(PIN_BUTTON) == GPIO.LOW:
            print("Button pressed!")
            
            # Wait for button release to avoid multiple detections
            while GPIO.input(PIN_BUTTON) == GPIO.LOW:
                time.sleep(0.01)
            
            # Small delay after release
            time.sleep(0.1)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nProgram interrupted")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")