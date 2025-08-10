#!/usr/bin/env python3
# filepath: /home/user/my-iot-scripts/vibration_sensor_test.py

import RPi.GPIO as GPIO
import time
from datetime import datetime

# Configuration
VIBRATION_PIN = 17  # GPIO pin connected to DO pin
SENSITIVITY = 0.01  # Seconds between readings
RECORD_TIME = 3.0   # Seconds to record vibrations

def setup():
  """Initialize GPIO settings"""
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(VIBRATION_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  print("SW-420 vibration sensor initialized")

def basic_detection():
  """Basic vibration detection"""
  try:
    setup()
    print("\n=== SW-420 Vibration Sensor Test ===")
    print("Tap or shake the sensor to test")
    print("Adjust blue potentiometer for sensitivity")
    print("Press Ctrl+C to exit\n")
    
    vibration_count = 0
    
    while True:
      # When vibration detected, DO pin goes LOW
      if GPIO.input(VIBRATION_PIN) == 0:
        vibration_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] Vibration detected! #{vibration_count}")
        
        # Small delay to avoid multiple triggers
        time.sleep(0.1)
      
      # Small delay between readings
      time.sleep(SENSITIVITY)
      
  except KeyboardInterrupt:
    print(f"\n\nTotal vibrations: {vibration_count}")
  finally:
    GPIO.cleanup()

def real_time_monitor():
  """Visual real-time vibration monitor"""
  try:
    setup()
    print("\n=== Real-time Vibration Monitor ===")
    print("Visualizes vibration intensity")
    print("Press Ctrl+C to exit\n")
    
    window_size = 20
    vibration_history = [0] * window_size
    
    while True:
      # Shift history left
      vibration_history = vibration_history[1:] + [0]
      
      # Check for vibration (LOW = vibration)
      if GPIO.input(VIBRATION_PIN) == 0:
        vibration_history[-1] = 1
      
      # Create visual bar
      bar = ""
      for v in vibration_history:
        bar += "█" if v else "░"
      
      # Calculate "intensity" based on recent vibrations
      intensity = sum(vibration_history) / window_size * 100
      
      # Print real-time bar
      print(f"\r{bar} {intensity:3.0f}%", end="", flush=True)
      
      # Small delay between readings
      time.sleep(SENSITIVITY)
      
  except KeyboardInterrupt:
    print("\n\nMonitoring stopped")
  finally:
    GPIO.cleanup()

def sensitivity_test():
  """Help adjust sensitivity potentiometer"""
  try:
    setup()
    print("\n=== Sensitivity Adjustment Mode ===")
    print("Turn blue potentiometer while testing")
    print("Press Ctrl+C when sensitivity is good\n")
    
    print("Current state: ", end="")
    
    while True:
      state = GPIO.input(VIBRATION_PIN)
      
      # Show current state
      if state == 0:
        print("\rState: TRIGGERED (vibration)   ", 
              end="", flush=True)
      else:
        print("\rState: NORMAL (no vibration)   ", 
              end="", flush=True)
      
      time.sleep(0.05)
      
  except KeyboardInterrupt:
    print("\n\nSensitivity adjustment complete")
  finally:
    GPIO.cleanup()

def vibration_recorder():
  """Record vibration pattern"""
  try:
    setup()
    print("\n=== Vibration Pattern Recorder ===")
    print(f"Records vibrations for {RECORD_TIME} seconds")
    print("Press Ctrl+C to exit\n")
    
    while True:
      input("Press Enter to start recording...")
      
      print("3...")
      time.sleep(1)
      print("2...")
      time.sleep(1)
      print("1...")
      time.sleep(1)
      print("GO! (tap pattern now)")
      
      # Record start time
      start_time = time.time()
      
      # Recording variables
      recording = []
      last_state = 1  # Start with no vibration
      
      # Record for set time
      while time.time() - start_time < RECORD_TIME:
        current_state = GPIO.input(VIBRATION_PIN)
        
        # If state changed
        if current_state != last_state:
          # Record time and new state
          event_time = time.time() - start_time
          recording.append((event_time, current_state))
          last_state = current_state
          
          # Visual feedback
          print("!" if current_state == 0 else ".", 
                end="", flush=True)
        
        time.sleep(SENSITIVITY)
      
      # Show recording results
      print("\n\nRecording complete!")
      print(f"Captured {len(recording)} state changes")
      
      # Display pattern
      print("\nPattern timeline:")
      print("0.0" + "-" * 50 + f"{RECORD_TIME:.1f}s")
      
      # Create timeline visualization
      timeline = [" "] * 50
      for time_point, state in recording:
        position = int((time_point / RECORD_TIME) * 49)
        timeline[position] = "V" if state == 0 else "^"
      
      print("".join(timeline))
      
      print("\nData points:")
      for i, (event_time, state) in enumerate(recording):
        event_type = "Vibration" if state == 0 else "Stopped"
        print(f"{i+1}. {event_type} at {event_time:.3f}s")
      
      print("\n" + "-" * 40)
      
  except KeyboardInterrupt:
    print("\n\nRecorder stopped")
  finally:
    GPIO.cleanup()

def security_monitor():
  """Simple security monitor"""
  try:
    setup()
    print("\n=== Security Monitor ===")
    print("Detects vibrations/movement")
    print("Press Ctrl+C to exit\n")
    
    # Get current time as start time
    start_time = time.time()
    last_detection = start_time
    events = []
    
    print("Monitoring started...")
    
    while True:
      if GPIO.input(VIBRATION_PIN) == 0:
        current_time = time.time()
        
        # If it's been more than 3 seconds since last detection
        if current_time - last_detection > 3:
          # Record this event
          timestamp = datetime.now()
          events.append(timestamp)
          
          # Show alert
          elapsed = current_time - start_time
          elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
          
          print(f"\n[{timestamp.strftime('%H:%M:%S')}] " + 
                f"Movement detected! ({elapsed_str} elapsed)")
          
          # Update last detection time
          last_detection = current_time
      
      # Show heartbeat to indicate monitoring
      elapsed = int(time.time() - start_time) % 10
      if elapsed == 0:
        print(".", end="", flush=True)
      
      time.sleep(0.1)
      
  except KeyboardInterrupt:
    print("\n\nMonitoring stopped")
    print(f"Total events: {len(events)}")
    
    if events:
      print("\nEvent log:")
      for i, event in enumerate(events):
        print(f"{i+1}. {event.strftime('%H:%M:%S')}")
  
  finally:
    GPIO.cleanup()

if __name__ == "__main__":
  print("\nSW-420 Vibration Sensor Menu:")
  print("1. Basic vibration detection")
  print("2. Real-time vibration monitor")
  print("3. Sensitivity adjustment")
  print("4. Vibration pattern recorder")
  print("5. Security monitor")
  
  choice = input("\nSelect mode (1-5): ")
  
  if choice == "2":
    real_time_monitor()
  elif choice == "3":
    sensitivity_test()
  elif choice == "4":
    vibration_recorder()
  elif choice == "5":
    security_monitor()
  else:
    basic_detection()