import RPi.GPIO as GPIO
import time

# right wheel
in1A = 8
in2A = 23
#enA = 3


def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(in1A, GPIO.OUT)
	GPIO.setup(in2A, GPIO.OUT)
	#GPIO.setup(enA, GPIO.OUT)
	
	
def forward(st):
    setup()
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    #GPIO.output(in1A, False)
    #GPIO.output(in2A, True)
    time.sleep(st)
	

print("forward")
forward(4)
GPIO.cleanup();
