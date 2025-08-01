#!/usr/bin/env python3
# filepath: /home/user/my-iot-scripts/tilt_switch_test.py

import RPi.GPIO as GPIO
import time
from datetime import datetime

TILT_PIN = 17  # Connect S pin to this GPIO

def setup():
  """Initialize GPIO settings"""
  GPIO.setmode(GPIO.BCM)
  # Pull-up resistor - sensor pulls LOW when tilted
  GPIO.setup(TILT_PIN, GPIO.IN, 
             pull_up_down=GPIO.PUD_UP)
  print("Tilt switch initialized")

def basic_tilt_detection():
  """Basic tilt detection"""
  try:
    setup()
    print("\n=== Tilt Switch Test ===")
    print("Tilt the sensor to test")
    print("Press Ctrl+C to exit\n")
    
    previous_state = None
    
    while True:
      current_state = GPIO.input(TILT_PIN)
      
      if current_state != previous_state:
        if current_state == 0:
          print("TILTED! ↗️")
        else:
          print("Level   ━")
        
        previous_state = current_state
      
      time.sleep(0.1)
      
  except KeyboardInterrupt:
    print("\n\nTest stopped")
  finally:
    GPIO.cleanup()

def orientation_monitor():
  """Monitor orientation continuously"""
  try:
    setup()
    print("\n=== Orientation Monitor ===")
    print("Shows real-time tilt status")
    print("Press Ctrl+C to exit\n")
    
    while True:
      state = GPIO.input(TILT_PIN)
      
      if state == 0:
        print("\r↗️ TILTED    ", end="", flush=True)
      else:
        print("\r━ LEVEL     ", end="", flush=True)
      
      time.sleep(0.05)
      
  except KeyboardInterrupt:
    print("\n\nMonitor stopped")
  finally:
    GPIO.cleanup()

def angle_finder():
  """Find trigger angle"""
  try:
    setup()
    print("\n=== Angle Finder ===")
    print("Slowly tilt to find trigger angle")
    print("Press SPACE when tilted, ENTER when level")
    print("Press Ctrl+C to exit\n")
    
    trigger_count = 0
    
    while True:
      state = GPIO.input(TILT_PIN)
      status = "TILTED" if state == 0 else "LEVEL"
      
      print(f"\rCurrent: {status} | Triggers: {trigger_count}",
            end="", flush=True)
      
      # Count state changes
      if state == 0:
        time.sleep(0.5)
        if GPIO.input(TILT_PIN) == 0:
          trigger_count += 1
      
      time.sleep(0.05)
      
  except KeyboardInterrupt:
    print(f"\n\nTotal triggers: {trigger_count}")
  finally:
    GPIO.cleanup()

def theft_alarm():
  """Simple theft/movement alarm"""
  try:
    setup()
    print("\n=== Theft Alarm Mode ===")
    print("Place on object to protect")
    print("Alarm triggers on movement")
    print("Press Ctrl+C to exit\n")
    
    # Wait for stable position
    print("Stabilizing...", end="", flush=True)
    time.sleep(3)
    print(" ARMED!")
    
    # Get initial state
    initial_state = GPIO.input(TILT_PIN)
    alarm_triggered = False
    
    while True:
      current_state = GPIO.input(TILT_PIN)
      
      # Detect any change from initial state
      if current_state != initial_state and not alarm_triggered:
        print("\n🚨 ALARM! MOVEMENT DETECTED! 🚨")
        print(f"Time: {datetime.now()}")
        alarm_triggered = True
        
        # Sound alarm (visual)
        for _ in range(20):
          print("!", end="", flush=True)
          time.sleep(0.1)
        
        print("\n\nPress Ctrl+C to reset")
      
      time.sleep(0.05)
      
  except KeyboardInterrupt:
    print("\n\nAlarm disarmed")
  finally:
    GPIO.cleanup()

def washing_machine_monitor():
  """Detect washing machine completion"""
  try:
    setup()
    print("\n=== Washing Machine Monitor ===")
    print("Attach to washing machine")
    print("Detects when vibration stops")
    print("Press Ctrl+C to exit\n")
    
    vibration_count = 0
    quiet_time = 0
    running = False
    
    while True:
      state = GPIO.input(TILT_PIN)
      
      # Count vibrations
      if state == 0:
        vibration_count += 1
        quiet_time = 0
        
        if not running and vibration_count > 5:
          print("\n🌊 Washing started!")
          running = True
      else:
        quiet_time += 1
      
      # Check if stopped (30 sec quiet)
      if running and quiet_time > 600:  # 30 sec
        print("\n✅ Washing complete!")
        running = False
        vibration_count = 0
      
      # Status display
      if running:
        print(f"\r🌊 Running... ({vibration_count} vibes)",
              end="", flush=True)
      else:
        print(f"\r⏸️  Idle", end="", flush=True)
      
      time.sleep(0.05)
      
  except KeyboardInterrupt:
    print("\n\nMonitor stopped")
  finally:
    GPIO.cleanup()

if __name__ == "__main__":
  print("\nKY-020 Tilt Switch Test")
  print("1. Basic tilt detection")
  print("2. Orientation monitor")
  print("3. Angle finder")
  print("4. Theft alarm")
  print("5. Washing machine monitor")
  
  choice = input("\nSelect mode (1-5): ")
  
  if choice == "2":
    orientation_monitor()
  elif choice == "3":
    angle_finder()
  elif choice == "4":
    theft_alarm()
  elif choice == "5":
    washing_machine_monitor()
  else:
    basic_tilt_detection()