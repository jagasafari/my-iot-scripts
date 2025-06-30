import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    print("Simple button test - one message per press")
    print("Press Ctrl+C to exit")
    
    while True:
        # Wait for button press
        if GPIO.input(18) == GPIO.LOW:
            print("Button pressed!")
            
            # Wait for button release to avoid multiple detections
            while GPIO.input(18) == GPIO.LOW:
                time.sleep(0.01)
            
            # Small delay after release
            time.sleep(0.1)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nProgram interrupted")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")