import RPi.GPIO as GPIO
import time

# right wheel
in1A = 8
in2A = 23
# left wheel
in3B = 17
in4B = 27


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1A, GPIO.OUT)
    GPIO.setup(in2A, GPIO.OUT)
    GPIO.setup(in3B, GPIO.OUT)
    GPIO.setup(in4B, GPIO.OUT)


def forward(st):
    setup()
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    time.sleep(st)


print("forward")
forward(4)
GPIO.cleanup()
