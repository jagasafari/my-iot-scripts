import RPi.GPIO as GPIO
import time

class IRTransmitter:
    def __init__(self, ir_pin=17):  # Use a different pin than receiver
        self.ir_pin = ir_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ir_pin, GPIO.OUT)
        GPIO.output(self.ir_pin, GPIO.LOW)
    
    def send_pulse(self, duration_us):
        """Send a 38kHz modulated pulse for specified microseconds"""
        # 38kHz = 26.3us period (13.15us on, 13.15us off)
        cycles = int(duration_us / 26.3)
        
        for _ in range(cycles):
            GPIO.output(self.ir_pin, GPIO.HIGH)
            time.sleep(0.0000131)  # 13.1us
            GPIO.output(self.ir_pin, GPIO.LOW)
            time.sleep(0.0000131)  # 13.1us
    
    def send_space(self, duration_us):
        """Send space (no signal) for specified microseconds"""
        GPIO.output(self.ir_pin, GPIO.LOW)
        time.sleep(duration_us / 1000000.0)
    
    def send_test_pattern(self):
        """Send a simple test pattern that can be detected by receiver"""
        print("Sending test pattern...")
        
        # Send a simple pattern: long pulse, short space, short pulse
        self.send_pulse(9000)   # 9ms pulse (common in NEC protocol)
        self.send_space(4500)   # 4.5ms space
        
        # Send some data bits
        for i in range(8):
            self.send_pulse(560)    # 560us pulse
            if i % 2 == 0:
                self.send_space(560)    # "0" bit
            else:
                self.send_space(1690)   # "1" bit
        
        # End pulse
        self.send_pulse(560)
        print("Test pattern sent!")
    
    def send_continuous_test(self, duration=5):
        """Send continuous pulses for testing with phone camera"""
        print(f"Sending continuous IR signal for {duration} seconds...")
        print("Point your phone camera at the IR LED to see if it's flashing!")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Simple on/off pattern visible to phone cameras
            GPIO.output(self.ir_pin, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(self.ir_pin, GPIO.LOW)
            time.sleep(0.1)
        
        print("Test complete!")
    
    def cleanup(self):
        GPIO.cleanup()

def test_with_receiver():
    """Test script to use with your IR receiver"""
    print("\n=== IR Transmitter/Receiver Test ===")
    print("1. Run your ir.py receiver script on another terminal")
    print("2. Position the transmitter pointing at the receiver")
    print("3. This script will send test signals\n")
    
    transmitter = IRTransmitter(ir_pin=17)  # Adjust pin as needed
    
    try:
        while True:
            print("\n--- Test Menu ---")
            print("1. Send test pattern")
            print("2. Phone camera test (continuous)")
            print("3. Send repeated pulses")
            print("4. Exit")
            
            choice = input("Enter choice: ").strip()
            
            if choice == "1":
                transmitter.send_test_pattern()
                time.sleep(1)
            
            elif choice == "2":
                transmitter.send_continuous_test()
            
            elif choice == "3":
                print("Sending repeated pulses for 10 seconds...")
                for i in range(10):
                    transmitter.send_test_pattern()
                    time.sleep(1)
                    print(f"Sent pulse {i+1}/10")
            
            elif choice == "4":
                break
                
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        transmitter.cleanup()

def simple_blink_test():
    """Ultra simple test - just blink the IR LED"""
    print("Simple IR LED blink test")
    print("Use your phone camera to see if IR LED is blinking\n")
    
    GPIO.setmode(GPIO.BCM)
    ir_pin = 17  # Adjust as needed
    GPIO.setup(ir_pin, GPIO.OUT)
    
    try:
        for i in range(20):
            GPIO.output(ir_pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(ir_pin, GPIO.LOW)
            time.sleep(0.5)
            print(f"Blink {i+1}/20")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    print("IR Transmitter Test\n")
    print("Module pinout (based on image):")
    print("  S  = Signal (connect to GPIO)")
    print("  +  = VCC (3.3V or 5V)")
    print("  -  = GND")
    print("\nMake sure connections are:")
    print("  S -> GPIO17 (or your chosen pin)")
    print("  + -> 3.3V or 5V")
    print("  - -> GND\n")
    
    mode = input("Select test mode:\n1. Full test\n2. Simple blink test\nChoice: ").strip()
    
    if mode == "2":
        simple_blink_test()
    else:
        test_with_receiver()