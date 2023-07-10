import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


pin_number = 17


GPIO.setup(pin_number, GPIO.IN)
GPIO.cleanup()
