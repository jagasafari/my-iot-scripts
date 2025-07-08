import RPi.GPIO as GPIO
import time
import json
from datetime import datetime

class IRLearner:
    def __init__(self, ir_pin=18):
        self.ir_pin = ir_pin
        self.learned_codes = {}
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def capture_ir_signal(self, timeout=10):
        """Capture raw IR signal timings"""
        print(f"Ready to learn IR signal. Press button within {timeout} seconds...")
        
        start_time = time.time()
        pulses = []
        
        # Wait for initial signal
        while GPIO.input(self.ir_pin) == 1:
            if time.time() - start_time > timeout:
                print("Timeout waiting for signal")
                return None
        
        # Capture pulse timings
        last_time = time.time()
        last_state = 0
        
        while time.time() - start_time < timeout:
            current_state = GPIO.input(self.ir_pin)
            current_time = time.time()
            
            if current_state != last_state:
                pulse_duration = (current_time - last_time) * 1000000  # microseconds
                pulses.append(int(pulse_duration))
                last_time = current_time
                last_state = current_state
                
                # Stop if we have enough data and signal is idle
                if len(pulses) > 50 and current_state == 1:
                    break
        
        return pulses if len(pulses) > 10 else None
    
    def learn_command(self, command_name):
        """Learn a specific IR command"""
        print(f"\nLearning command: {command_name}")
        
        # Capture multiple samples for accuracy
        samples = []
        for i in range(3):
            print(f"Sample {i+1}/3 - Press the button now...")
            signal = self.capture_ir_signal()
            if signal:
                samples.append(signal)
                print(f"Captured signal with {len(signal)} pulses")
                time.sleep(2)
            else:
                print("Failed to capture signal")
                return False
        
        if len(samples) >= 2:
            # Use the first successful capture
            self.learned_codes[command_name] = {
                'pulses': samples[0],
                'learned_at': datetime.now().isoformat(),
                'protocol': self.detect_protocol(samples[0])
            }
            print(f"Successfully learned command: {command_name}")
            return True
        else:
            print(f"Failed to learn command: {command_name}")
            return False
    
    def detect_protocol(self, pulses):
        """Simple protocol detection based on pulse patterns"""
        if not pulses:
            return "unknown"
        
        # Check for common IR protocols based on timing
        header = pulses[0] if len(pulses) > 0 else 0
        
        if 8000 < header < 10000:  # ~9ms header
            return "NEC"
        elif 2000 < header < 3000:  # ~2.4ms header
            return "Sony"
        elif 3000 < header < 4000:  # ~3.6ms header
            return "RC5"
        else:
            return "unknown"
    
    def save_learned_codes(self, filename="learned_ir_codes.json"):
        """Save learned codes to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.learned_codes, f, indent=2)
            print(f"Saved learned codes to {filename}")
        except Exception as e:
            print(f"Error saving codes: {e}")
    
    def load_learned_codes(self, filename="learned_ir_codes.json"):
        """Load previously learned codes"""
        try:
            with open(filename, 'r') as f:
                self.learned_codes = json.load(f)
            print(f"Loaded {len(self.learned_codes)} learned codes")
        except FileNotFoundError:
            print("No previous codes found")
        except Exception as e:
            print(f"Error loading codes: {e}")
    
    def list_learned_commands(self):
        """Display all learned commands"""
        if not self.learned_codes:
            print("No commands learned yet")
            return
        
        print("\nLearned commands:")
        for cmd, data in self.learned_codes.items():
            protocol = data.get('protocol', 'unknown')
            learned_at = data.get('learned_at', 'unknown')
            pulse_count = len(data.get('pulses', []))
            print(f"  {cmd}: {protocol} protocol, {pulse_count} pulses, learned: {learned_at}")
    
    def cleanup(self):
        """Clean up GPIO"""
        GPIO.cleanup()

def main():
    ir_learner = IRLearner(ir_pin=18)  # Change pin as needed
    
    try:
        ir_learner.load_learned_codes()
        
        while True:
            print("\n=== IR Learning Menu ===")
            print("1. Learn new command")
            print("2. List learned commands")
            print("3. Save codes to file")
            print("4. Exit")
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                command_name = input("Enter command name: ").strip()
                if command_name:
                    ir_learner.learn_command(command_name)
                else:
                    print("Invalid command name")
            
            elif choice == "2":
                ir_learner.list_learned_commands()
            
            elif choice == "3":
                ir_learner.save_learned_codes()
            
            elif choice == "4":
                break
            
            else:
                print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\nExiting...")
    
    finally:
        ir_learner.save_learned_codes()
        ir_learner.cleanup()

if __name__ == "__main__":
    main()