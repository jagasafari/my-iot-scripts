#!/usr/bin/env python3
"""
LED Diagnostic Script
This script helps diagnose common LED issues with Raspberry Pi GPIO
"""
import RPi.GPIO as GPIO
import time

# Pin definition
PIN_LED = 23

def check_gpio_setup():
    """Check basic GPIO setup"""
    print("=== GPIO Diagnostic ===")
    
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_LED, GPIO.OUT)
    
    print(f"GPIO pin {PIN_LED} configured as output")
    
    # Test basic on/off
    print("Testing basic digital output...")
    print("  - Setting pin HIGH")
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(2)
    
    print("  - Setting pin LOW")
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(1)
    
    print("Basic digital test complete")

def test_pwm_frequencies():
    """Test different PWM frequencies"""
    print("\n=== PWM Frequency Test ===")
    
    frequencies = [100, 500, 1000, 2000, 5000]
    
    for freq in frequencies:
        print(f"Testing PWM at {freq}Hz...")
        pwm = GPIO.PWM(PIN_LED, freq)
        pwm.start(0)
        
        # Ramp up to 100%
        for duty in range(0, 101, 10):
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
        
        # Hold at 100% for observation
        time.sleep(1)
        
        # Ramp down
        for duty in range(100, -1, -10):
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
        
        pwm.stop()
        time.sleep(0.5)

def test_duty_cycles():
    """Test specific duty cycles to identify brightness issues"""
    print("\n=== Duty Cycle Test ===")
    
    pwm = GPIO.PWM(PIN_LED, 1000)
    pwm.start(0)
    
    duty_cycles = [10, 25, 50, 75, 90, 100]
    
    for duty in duty_cycles:
        print(f"  - Testing {duty}% duty cycle for 3 seconds")
        pwm.ChangeDutyCycle(duty)
        time.sleep(3)
    
    pwm.ChangeDutyCycle(0)
    pwm.stop()

def voltage_level_test():
    """Simulate different voltage levels using PWM"""
    print("\n=== Voltage Level Simulation ===")
    print("This simulates different effective voltages using PWM")
    
    pwm = GPIO.PWM(PIN_LED, 1000)
    pwm.start(0)
    
    # Test different "voltage" levels
    voltage_levels = [
        (25, "~0.8V equivalent"),
        (50, "~1.6V equivalent"), 
        (75, "~2.4V equivalent"),
        (100, "~3.3V equivalent")
    ]
    
    for duty, description in voltage_levels:
        print(f"  - {description} ({duty}% duty)")
        pwm.ChangeDutyCycle(duty)
        time.sleep(3)
    
    pwm.ChangeDutyCycle(0)
    pwm.stop()

def main():
    """Main diagnostic routine"""
    print("LED Diagnostic Tool")
    print("===================")
    print("This will help diagnose LED brightness issues")
    print("Watch your LED carefully during each test")
    print("Press Ctrl+C to exit at any time\n")
    
    try:
        # Basic GPIO test
        check_gpio_setup()
        
        # PWM frequency test
        test_pwm_frequencies()
        
        # Duty cycle test
        test_duty_cycles()
        
        # Voltage level test
        voltage_level_test()
        
        print("\n=== Diagnostic Complete ===")
        print("If your LED is still dim, possible causes:")
        print("1. LED module requires external power supply")
        print("2. LED is designed for higher voltage (5V instead of 3.3V)")
        print("3. Current limiting resistor is too high")
        print("4. LED module is damaged")
        print("5. Wiring issue (check connections)")
        
    except KeyboardInterrupt:
        print("\nDiagnostic interrupted by user")
    
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up")

if __name__ == "__main__":
    main()
