#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from datetime import datetime

KNOCK_SENSOR_PIN = 17

def setup():
  """Initialize GPIO settings"""
  GPIO.setmode(GPIO.BCM)
  # Pull-up because sensor goes LOW on knock
  GPIO.setup(KNOCK_SENSOR_PIN, GPIO.IN, 
             pull_up_down=GPIO.PUD_UP)
  print("Knock sensor initialized")

def basic_detection():
  """Basic knock detection"""
  try:
    setup()
    print("\n=== Knock Sensor Test ===")
    print("Tap the sensor or surface nearby")
    print("Press Ctrl+C to exit\n")
    
    knock_count = 0
    
    while True:
      # Sensor outputs LOW when knocked
      if GPIO.input(KNOCK_SENSOR_PIN) == 0:
        knock_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Knock detected! #{knock_count}")
        
        # Wait to avoid multiple detections
        time.sleep(0.2)
      
      # Small delay to reduce CPU usage
      time.sleep(0.01)
      
  except KeyboardInterrupt:
    print(f"\n\nTotal knocks: {knock_count}")
  finally:
    GPIO.cleanup()

def pattern_detector():
  """Detect knock patterns"""
  try:
    setup()
    print("\n=== Knock Pattern Detector ===")
    print("Try knocking patterns like:")
    print("- 2 knocks = Double tap")
    print("- 3 knocks = Triple tap")
    print("Press Ctrl+C to exit\n")
    
    knocks = []
    last_knock_time = 0
    
    while True:
      if GPIO.input(KNOCK_SENSOR_PIN) == 0:
        current_time = time.time()
        
        # If more than 1 second since last knock
        # analyze previous pattern
        if current_time - last_knock_time > 1.0:
          if len(knocks) > 0:
            analyze_pattern(knocks)
          knocks = []
        
        knocks.append(current_time)
        last_knock_time = current_time
        print("*", end="", flush=True)
        
        # Debounce
        time.sleep(0.15)
      
      # Check for pattern timeout
      if knocks and time.time() - last_knock_time > 1.0:
        analyze_pattern(knocks)
        knocks = []
      
      time.sleep(0.01)
      
  except KeyboardInterrupt:
    print("\n\nPattern detection stopped")
  finally:
    GPIO.cleanup()

def analyze_pattern(knocks):
  """Analyze knock pattern"""
  count = len(knocks)
  print(f"\nPattern: {count} knocks")
  
  if count == 1:
    print("→ Single tap")
  elif count == 2:
    print("→ Double tap")
  elif count == 3:
    print("→ Triple tap")
  elif count == 4:
    print("→ Quadruple tap")
  else:
    print(f"→ Complex pattern ({count} taps)")

def sensitivity_monitor():
  """Monitor sensitivity continuously"""
  try:
    setup()
    print("\n=== Sensitivity Monitor ===")
    print("Shows sensor state in real-time")
    print("Adjust spring tension if needed")
    print("Press Ctrl+C to exit\n")
    
    while True:
      state = GPIO.input(KNOCK_SENSOR_PIN)
      
      if state == 0:
        print("\r[KNOCKED] ████████", end="", flush=True)
      else:
        print("\r[READY]   --------", end="", flush=True)
      
      time.sleep(0.02)
      
  except KeyboardInterrupt:
    print("\n\nMonitoring stopped")
  finally:
    GPIO.cleanup()

def vibration_alarm():
  """Vibration alarm mode"""
  try:
    setup()
    print("\n=== Vibration Alarm ===")
    print("Detects any vibration/movement")
    print("Place on door, window, or object")
    print("Press Ctrl+C to exit\n")
    
    print("Alarm ARMED - Monitoring...")
    triggered = False
    
    while True:
      if GPIO.input(KNOCK_SENSOR_PIN) == 0:
        if not triggered:
          print("\n⚠️  ALARM! Vibration detected! ⚠️")
          print("Time:", datetime.now())
          triggered = True
          
          # Alarm for 3 seconds
          for i in range(30):
            print("!", end="", flush=True)
            time.sleep(0.1)
          
          print("\n\nRe-armed...")
          triggered = False
      
      time.sleep(0.01)
      
  except KeyboardInterrupt:
    print("\n\nAlarm disarmed")
  finally:
    GPIO.cleanup()

if __name__ == "__main__":
  print("\nKnock Sensor Test Options:")
  print("1. Basic knock detection")
  print("2. Pattern detection")
  print("3. Sensitivity monitor")
  print("4. Vibration alarm")
  
  choice = input("\nSelect mode (1-4): ")
  
  if choice == "2":
    pattern_detector()
  elif choice == "3":
    sensitivity_monitor()
  elif choice == "4":
    vibration_alarm()
  else:
    basic_detection()