#!/usr/bin/env python3
"""
LED Wiring and Hardware Check
Helps identify common hardware issues with LED modules
"""
import RPi.GPIO as GPIO
import time

# Pin definition
PIN_LED = 23

def basic_continuity_test():
    """Test basic GPIO output functionality"""
    print("=== Basic Continuity Test ===")
    print("This test rapidly toggles the GPIO pin")
    print("You should see the LED flickering if wiring is correct")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_LED, GPIO.OUT)
    
    print("Starting rapid toggle test for 10 seconds...")
    start_time = time.time()
    
    while time.time() - start_time < 10:
        GPIO.output(PIN_LED, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(PIN_LED, GPIO.LOW)
        time.sleep(0.1)
    
    print("Rapid toggle test complete")

def power_supply_test():
    """Test if LED needs external power"""
    print("\n=== Power Supply Test ===")
    print("Testing if your LED module might need external power")
    
    pwm = GPIO.PWM(PIN_LED, 1000)
    pwm.start(0)
    
    print("Setting LED to maximum brightness...")
    pwm.ChangeDutyCycle(100)
    
    print("If LED is still very dim, it might need:")
    print("- External 5V power supply")
    print("- Higher current than GPIO pin can provide")
    print("- Different wiring configuration")
    
    time.sleep(5)
    pwm.stop()

def led_type_identification():
    """Help identify LED module type"""
    print("\n=== LED Module Type Check ===")
    print("Please check your LED module and answer these questions:")
    print("1. Does it have 3 pins? (VCC, GND, Signal)")
    print("2. Does it have built-in resistors?")
    print("3. What voltage is it rated for? (3.3V or 5V)")
    print("4. Is it a single LED or LED array?")
    print("5. Does it have any markings or part numbers?")
    print("\nCommon LED modules:")
    print("- KY-016: 3-color RGB LED (needs 3 pins)")
    print("- Basic LED: Single color, might need resistor")
    print("- LED strip: Usually needs external power")
    print("- High-power LED: Definitely needs external power")

def troubleshooting_guide():
    """Provide troubleshooting steps"""
    print("\n=== Troubleshooting Guide ===")
    print("If your LED is barely visible (red dot), try these solutions:")
    print()
    print("1. WIRING CHECK:")
    print("   - LED+ (long leg) → GPIO23 (pin 16)")
    print("   - LED- (short leg) → GND (pin 6, 9, 14, 20, 25, 30, 34, or 39)")
    print("   - If using a module: VCC→3.3V, GND→GND, Signal→GPIO23")
    print()
    print("2. VOLTAGE ISSUES:")
    print("   - Your LED might be designed for 5V instead of 3.3V")
    print("   - Try connecting VCC to 5V pin (pin 2 or 4) instead of 3.3V")
    print()
    print("3. CURRENT LIMITING:")
    print("   - If using bare LED, add 220Ω resistor in series")
    print("   - If module has built-in resistor, it might be too high")
    print()
    print("4. LED ORIENTATION:")
    print("   - Make sure LED is not inserted backwards")
    print("   - Long leg (anode) should go to positive")
    print()
    print("5. EXTERNAL POWER:")
    print("   - Some LED modules need external power supply")
    print("   - Connect external 5V to VCC, common GND")

def main():
    print("LED Hardware Diagnostic")
    print("======================")
    
    try:
        basic_continuity_test()
        power_supply_test()
        led_type_identification()
        troubleshooting_guide()
        
    except KeyboardInterrupt:
        print("\nDiagnostic interrupted")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
