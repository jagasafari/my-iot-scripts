#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# ───── Pin Definitions ─────
PIN_BLUE  = 17
PIN_GREEN = 27
PIN_RED   = 22

# ───── Setup ─────
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in (PIN_BLUE, PIN_GREEN, PIN_RED):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)      # LOW = off  <<<< changed
    #GPIO.output(pin, GPIO.HIGH)  # HIGH =ls on rasberry py baord vs gpio /or gpio vs 3v and 5v under thewhat is aoff (common-cathode)

def set_color(r: bool, g: bool, b: bool):
    """Drive each channel HIGH to light, LOW to turn off."""
    GPIO.output(PIN_RED,   GPIO.HIGH if r else GPIO.LOW)   # <<<< swapped
    GPIO.output(PIN_GREEN, GPIO.HIGH if g else GPIO.LOW)
    GPIO.output(PIN_BLUE,  GPIO.HIGH if b else GPIO.LOW)
#    """Drive each channel LOW to light, HIGH to turn off."""
#    GPIO.output(PIN_RED,   GPIO.LOW  if r else GPIO.HIGH)
#    GPIO.output(PIN_GREEN, GPIO.LOW  if g else GPIO.HIGH)
#    GPIO.output(PIN_BLUE,  GPIO.LOW  if b else GPIO.HIGH)

def fade_color(pin, duration=1.0, steps=50):
    """Simple software PWM fade on single pin."""
    for i in range(steps + 1):
        duty = i / steps
        # ON time = duty, OFF = (1-duty)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(duty * duration / steps)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep((1 - duty) * duration / steps)

try:
    while True:
        # Static colors
        for name, vals in [("Red",   (1,0,0)),
                           ("Green", (0,1,0)),
                           ("Blue",  (0,0,1)),
                           ("White", (1,1,1)),
                           ("Off",   (0,0,0))]:
            print(f"Setting {name}")
            set_color(*vals)
            time.sleep(4.0)

        # Fade Red → Green → Blue
        print("Fading each channel…")
        for pin in (PIN_RED, PIN_GREEN, PIN_BLUE):
            fade_color(pin, duration=1.5)
            time.sleep(1.5)

except KeyboardInterrupt:
    pass

finally:
    # ───── Cleanup ─────
    set_color(0,0,0)
    GPIO.cleanup()
    print("GPIO cleaned up, exiting.")
