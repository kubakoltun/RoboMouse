import RPi.GPIO as GPIO
import time

# right wheel
in1A = 8
in2A = 23
enA = 3


def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(in1A, GPIO.OUT)
	GPIO.setup(in2A, GPIO.OUT)
	GPIO.setup(enA, GPIO.OUT)
	
	
def loop():
	while True:
		GPIO.output(in1A, GPIO.LOW)
		GPIO.output(in2A, GPIO.HIGH)
		GPIO.output(enA, GPIO.HIGH)
		time.sleep(2)
		
		GPIO.output(in1A, GPIO.HIGH)
		GPIO.output(in2A, GPIO.LOW)
		GPIO.output(enA, GPIO.HIGH)
		time.sleep(2)


try:
	setup()
	loop()
except KeyboardInterrupt:
		GPIO.cleanup();
