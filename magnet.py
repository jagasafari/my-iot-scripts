#!/usr/bin/env python3
# filepath: /home/user/my-iot-scripts/magnet_detector.py

import RPi.GPIO as GPIO
import time
import datetime

# Configuration
HALL_SENSOR_PIN = 17  # GPIO pin connected to the Hall sensor's signal pin (S)
LED_PIN = 27          # Optional: Connect an LED to this pin to show detection
BUZZER_PIN = 22       # Optional: Connect a buzzer for audible detection

# Detection settings
LOG_FILE = "magnet_detections.log"
DEBOUNCE_TIME = 0.1   # Seconds to wait between readings to avoid false triggers

def setup():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    
    # Setup Hall sensor pin as input with pull-up resistor
    # (Hall sensor typically outputs LOW when magnet is detected)
    GPIO.setup(HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Optional: Setup LED and buzzer pins
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    # Initialize outputs to OFF
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    print("Magnet detector initialized")

def log_detection(state):
    """Log magnet detection events to file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "DETECTED" if state else "REMOVED"
    
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp}: Magnet {status}\n")
    
    print(f"{timestamp}: Magnet {status}")

def alert(state):
    """Trigger LED and buzzer based on detection state"""
    GPIO.output(LED_PIN, state)
    GPIO.output(BUZZER_PIN, state)
    
    # If using buzzer, make short beep
    if state:
        time.sleep(0.1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

def main():
    """Main program"""
    try:
        setup()
        print("\n=== Magnet Detector Test ===")
        print(f"Listening on GPIO pin {HALL_SENSOR_PIN}")
        print("Move a magnet near the sensor to test")
        print("Press Ctrl+C to exit\n")
        
        # Track previous state to detect changes
        previous_state = GPIO.input(HALL_SENSOR_PIN)
        
        # Create or clear log file
        with open(LOG_FILE, "w") as f:
            f.write("=== Magnet Detection Log ===\n")
        
        while True:
            # Read current state (LOW/FALSE = magnet detected for most Hall sensors)
            current_state = GPIO.input(HALL_SENSOR_PIN)
            
            # Check if state changed (magnet detected or removed)
            if current_state != previous_state:
                # Magnet detected (LOW) or removed (HIGH)
                magnet_present = not current_state  # Invert because LOW = detected
                
                # Log and alert
                log_detection(magnet_present)
                alert(magnet_present)
                
                # Update previous state
                previous_state = current_state
                
                # Debounce
                time.sleep(DEBOUNCE_TIME)
            
            # Small delay to reduce CPU usage
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    
    finally:
        # Turn off outputs and clean up
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup()
        print("GPIO cleanup completed")
        print(f"Detection log saved to {LOG_FILE}")

def continuous_monitoring():
    """Run the detection with continuous output"""
    try:
        setup()
        print("\n=== Continuous Magnet Field Monitoring ===")
        print("Press Ctrl+C to exit\n")
        
        while True:
            state = GPIO.input(HALL_SENSOR_PIN)
            magnet_present = not state  # Invert because LOW = detected
            
            if magnet_present:
                print("\rMagnet DETECTED ✓ ", end="", flush=True)
                GPIO.output(LED_PIN, GPIO.HIGH)
            else:
                print("\rNo magnet      ✗ ", end="", flush=True)
                GPIO.output(LED_PIN, GPIO.LOW)
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    
    finally:
        GPIO.cleanup()
        print("GPIO cleanup completed")

if __name__ == "__main__":
    print("\nChoose an option:")
    print("1. Detect and log magnet events")
    print("2. Continuous monitoring")
    
    choice = input("Enter choice (1-2): ")
    
    if choice == "2":
        continuous_monitoring()
    else:
        main()