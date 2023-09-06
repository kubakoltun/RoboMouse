import RPi.GPIO as GPIO
import time

left_wheel_pin1 = 23
left_wheel_pin2 = 24
left_en = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(left_wheel_pin1, GPIO.OUT)
GPIO.setup(left_wheel_pin2, GPIO.OUT)
GPIO.setup(left_en, GPIO.OUT)
GPIO.output(left_wheel_pin1, GPIO.LOW)
GPIO.output(left_wheel_pin2, GPIO.LOW)

pA = GPIO.PWM(left_en, 1000)
pA.start(25)


def move_forward():
	GPIO.output(left_wheel_pin1, GPIO.HIGH)
	GPIO.output(left_wheel_pin2, GPIO.LOW)
	

def move_backward():
	GPIO.output(left_wheel_pin1, GPIO.LOW)
	GPIO.output(left_wheel_pin2, GPIO.HIGH)
	
	
print("Moving forward")
move_forward()
time.sleep(2)


GPIO.cleanup()
