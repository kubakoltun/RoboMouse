import RPi.GPIO as GPIO
import time


left_wheel_pin1 = 23
left_wheel_pin2 = 24
left_en = 25

# right_wheel_pin1 = 8
# right_wheel_pin2 = 10
# rigth_en = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(left_wheel_pin1, GPIO.OUT)
GPIO.setup(left_wheel_pin2, GPIO.OUT)
GPIO.setup(left_en, GPIO.OUT)

GPIO.setup(right_wheel_pin1, GPIO.OUT)
GPIO.setup(right_wheel_pin2, GPIO.OUT)


def move_forward():
	GPIO.output(left_wheel_pin1, GPIO.HIGH)
	GPIO.output(left_wheel_pin2, GPIO.LOW)
	GPIO.output(right_wheel_pin1, GPIO.HIGH)
	GPIO.output(right_wheel_pin2, GPIO.LOW)
	

def move_backward():
	GPIO.output(left_wheel_pin1, GPIO.LOW)
	GPIO.output(left_wheel_pin2, GPIO.HIGH)
	GPIO.output(right_wheel_pin1, GPIO.LOW)
	GPIO.output(right_wheel_pin2, GPIO.HIGH)
	
	
def turn_left():
	GPIO.output(left_wheel_pin1, GPIO.LOW)
	GPIO.output(left_wheel_pin2, GPIO.HIGH)
	GPIO.output(right_wheel_pin1, GPIO.HIGH)
	GPIO.output(right_wheel_pin2, GPIO.LOW)
	

def turn_right():
	GPIO.output(left_wheel_pin1, GPIO.HIGH)
	GPIO.output(left_wheel_pin2, GPIO.LOW)
	GPIO.output(right_wheel_pin1, GPIO.LOW)
	GPIO.output(right_wheel_pin2, GPIO.HIGH)
	
	
def stop():
	GPIO.output(left_wheel_pin1, GPIO.LOW)
	GPIO.output(left_wheel_pin2, GPIO.LOW)
	GPIO.output(right_wheel_pin1, GPIO.LOW)
	GPIO.output(right_wheel_pin2, GPIO.LOW)
	
	
move_forward()
time.sleep(2)
stop()
time.sleep(1)
#turn_left()
#time.sleep(1)
stop()


GPIO.cleanup()
