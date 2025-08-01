#!/usr/bin/env python3
# filepath: /home/user/my-iot-scripts/tilt_sensor_test.py

import RPi.GPIO as GPIO
import time

# Configuration
TILT_PIN = 17  # Connect DO to this GPIO pin

def setup():
  """Initialize GPIO settings"""
  # Set GPIO mode
  GPIO.setmode(GPIO.BCM)
  
  # Setup tilt sensor pin as input with pull-up
  GPIO.setup(TILT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  
  print("Tilt sensor initialized")

def main():
  """Main program"""
  try:
    setup()
    
    print("\n=== Tilt Sensor Test ===")
    print("Tilt the sensor to test")
    print("Normal position vs tilted position")
    print("Press Ctrl+C to exit\n")
    
    # Track previous state to detect changes
    previous_state = None
    tilt_count = 0
    
    while True:
      # Read sensor state
      current_state = GPIO.input(TILT_PIN)
      
      # Check if state changed
      if current_state != previous_state:
        if current_state == 0:
          # Tilted (assuming active LOW)
          tilt_count += 1
          print(f"TILTED! #{tilt_count} 📐")
        else:
          # Normal position
          print("NORMAL position ⬜")
        
        previous_state = current_state
      
      # Small delay
      time.sleep(0.05)
      
  except KeyboardInterrupt:
    print(f"\n\nTotal tilts detected: {tilt_count}")
    print("Program interrupted by user")
  
  finally:
    # Cleanup
    GPIO.cleanup()
    print("GPIO cleanup completed")

def continuous_monitor():
  """Continuous monitoring mode"""
  try:
    setup()
    
    print("\n=== Continuous Tilt Monitor ===")
    print("Watch real-time tilt status")
    print("Press Ctrl+C to exit\n")
    
    while True:
      # Read current state
      state = GPIO.input(TILT_PIN)
      
      if state == 0:
        print("\rTILTED  📐", end="", flush=True)
      else:
        print("\rNORMAL  ⬜", end="", flush=True)
      
      time.sleep(0.1)
      
  except KeyboardInterrupt:
    print("\n\nProgram interrupted by user")
  
  finally:
    GPIO.cleanup()
    print("GPIO cleanup completed")

def sensitivity_test():
  """Test different tilt angles"""
  try:
    setup()
    
    print("\n=== Tilt Angle Test ===")
    print("Try different tilt angles")
    print("Find the trigger point")
    print("Press Ctrl+C when done\n")
    
    reading_count = 0
    while True:
      state = GPIO.input(TILT_PIN)
      reading_count += 1
      
      status = "TILTED" if state == 0 else "NORMAL"
      print(f"\rReading {reading_count}: {status}     ", 
            end="", flush=True)
      
      time.sleep(0.2)
      
  except KeyboardInterrupt:
    print("\n\nAngle testing complete")
  
  finally:
    GPIO.cleanup()

def shake_detector():
  """Detect shaking/vibration"""
  try:
    setup()
    
    print("\n=== Shake Detector ===")
    print("Shake the sensor to detect motion")
    print("Press Ctrl+C to exit\n")
    
    shake_count = 0
    last_change_time = time.time()
    
    previous_state = GPIO.input(TILT_PIN)
    
    while True:
      current_state = GPIO.input(TILT_PIN)
      current_time = time.time()
      
      # Detect state change (shake)
      if current_state != previous_state:
        time_diff = current_time - last_change_time
        
        # If rapid changes, consider it shaking
        if time_diff < 0.5:  # Less than 0.5 seconds
          shake_count += 1
          print(f"SHAKE detected! #{shake_count} 🟫")
        
        last_change_time = current_time
        previous_state = current_state
      
      time.sleep(0.01)
      
  except KeyboardInterrupt:
    print(f"\n\nTotal shakes detected: {shake_count}")
    print("Program interrupted by user")
  
  finally:
    GPIO.cleanup()

if __name__ == "__main__":
  print("\nChoose test mode:")
  print("1. Basic tilt detection")
  print("2. Continuous monitoring")
  print("3. Angle sensitivity test")
  print("4. Shake detector")
  
  choice = input("Enter choice (1-4): ")
  
  if choice == "2":
    continuous_monitor()
  elif choice == "3":
    sensitivity_test()
  elif choice == "4":
    shake_detector()
  else:
    main()
