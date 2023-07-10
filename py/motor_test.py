import RPi.GPIO as GPIO
import time

# right wheel
in1A = 8
in2A = 23
enA = 3
# left wheel
in3B = 17
in4B = 27
enB = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1A, GPIO.OUT)
GPIO.setup(in2A, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.output(in1A, GPIO.LOW)
GPIO.output(in2A, GPIO.LOW)

GPIO.setup(in3B, GPIO.OUT)
GPIO.setup(in4B, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
GPIO.output(in3B, GPIO.LOW)
GPIO.output(in4B, GPIO.LOW)

pA = GPIO.PWM(enA, 1000)
pA.start(25)
pB = GPIO.PWM(enB, 1000)
pB.start(25)


def move_forward():
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    GPIO.output(enB, GPIO.HIGH)


def move_backward():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    GPIO.output(enB, GPIO.HIGH)


def turn_left():
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    GPIO.output(enB, GPIO.HIGH)


def turn_right():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    GPIO.output(enB, GPIO.HIGH)


def stop():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(enA, GPIO.Low)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)
    GPIO.output(enB, GPIO.LOW)


print("forward")
move_forward()
time.sleep(2)

print("backwards")
move_backward()
time.sleep(2)

print("left")
turn_left()
time.sleep(2)

print("right")
turn_right()
time.sleep(2)

GPIO.cleanup()
