import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pin_number = int(input("Enter the GPIO pin number: ")) 
GPIO.setup(pin_number, GPIO.IN)
GPIO.cleanup()
