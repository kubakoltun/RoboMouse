import RPi.GPIO as GPIO

pin_number = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_number, GPIO.IN)
GPIO.cleanup()
