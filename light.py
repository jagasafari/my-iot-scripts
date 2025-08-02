#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

LIGHT_SENSOR_PIN = 17

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
  print("Light sensor initialized")

def main():
  try:
    setup()
    
    print("\n=== Light Sensor Test ===")
    print("Cover sensor with hand to test")
    print("Adjust blue potentiometer for sensitivity")
    print("Press Ctrl+C to exit\n")
    
    previous_state = None
    
    while True:
      # Read sensor state
      # Sensor is active HIGH (1=dark, 0=light)
      current_state = GPIO.input(LIGHT_SENSOR_PIN)
      
      if current_state != previous_state:
        if current_state == 1:  # Changed from 0 to 1
          # Dark detected (active HIGH)
          print("DARK detected! 🌙")
        else:
          print("LIGHT detected! ☀️")
        
        previous_state = current_state
      
      time.sleep(0.1)
      
  except KeyboardInterrupt:
    print("\n\nProgram interrupted by user")
  
  finally:
    GPIO.cleanup()
    print("GPIO cleanup completed")

def continuous_monitor():
  """Continuous monitoring mode"""
  try:
    setup()
    
    print("\n=== Continuous Light Monitor ===")
    print("Press Ctrl+C to exit\n")
    
    while True:
      # Read current state
      state = GPIO.input(LIGHT_SENSOR_PIN)
      
      if state == 0:
        print("\rDARK  🌙", end="", flush=True)
      else:
        print("\rLIGHT ☀️", end="", flush=True)
      
      time.sleep(0.2)
      
  except KeyboardInterrupt:
    print("\n\nProgram interrupted by user")
  
  finally:
    GPIO.cleanup()
    print("GPIO cleanup completed")

def sensitivity_test():
  """Help adjust sensitivity"""
  try:
    setup()
    
    print("\n=== Sensitivity Adjustment ===")
    print("Turn blue potentiometer while testing")
    print("Watch when LED on module turns on/off")
    print("Press Ctrl+C when satisfied\n")
    
    count = 0
    while True:
      state = GPIO.input(LIGHT_SENSOR_PIN)
      count += 1
      
      status = "TRIGGERED" if state == 0 else "NOT TRIGGERED"
      print(f"\rReading {count}: {status}     ", 
            end="", flush=True)
      
      time.sleep(0.3)
      
  except KeyboardInterrupt:
    print("\n\nSensitivity adjustment complete")
  
  finally:
    GPIO.cleanup()

if __name__ == "__main__":
  print("\nChoose test mode:")
  print("1. Basic light detection")
  print("2. Continuous monitoring")
  print("3. Sensitivity adjustment")
  
  choice = input("Enter choice (1-3): ")
  
  if choice == "2":
    continuous_monitor()
  elif choice == "3":
    sensitivity_test()
  else:
    main()