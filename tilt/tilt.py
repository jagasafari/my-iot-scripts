import RPi.GPIO as GPIO
import time

# Pin definitions
PIN_TILT = 18

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_TILT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Tilt Switch Module Test")
    print("Tilt the sensor to trigger it")
    print("Press Ctrl+C to exit")
    
    last_state = GPIO.input(PIN_TILT)
    print(f"Initial state: {'Tilted' if last_state == GPIO.LOW else 'Level'}")
    
    while True:
        current_state = GPIO.input(PIN_TILT)
        
        if current_state != last_state:
            if current_state == GPIO.LOW:
                print("TILTED! Switch activated")
            else:
                print("LEVEL - Switch deactivated")
            
            last_state = current_state
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram interrupted")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")