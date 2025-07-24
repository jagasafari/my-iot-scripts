python3 -c "import RPi.GPIO as GPIO; GPIO.cleanup()"
#Test basic GPIO:
python3 -c "import RPi.GPIO as GPIO; print('GPIO import successful')"
#Check if pin is stuck:
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.cleanup()"