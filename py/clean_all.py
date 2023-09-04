import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


all_pins = list(range(2, 29))

for pin in all_pins:
	GPIO.setup(pin, GPIO.OUT)

for pin in all_pins:
	GPIO.cleanup(pin)
