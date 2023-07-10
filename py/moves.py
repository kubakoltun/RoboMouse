import RPi.GPIO as GPIO
from time import sleep

# right wheel
in1A = 24
in2A = 23
enA = 25
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
# pA.start(25)

pB = GPIO.PWM(enB, 1000)
# pB.start(25)


def move_forward(pas, pab):
    pA.start(pas)
    pB.start(pab)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)


def move_backward(pas, pab):
    pA.start(pas)
    pB.start(pab)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)


def turn_left(pas, pab):
    pA.start(pas)
    pB.start(pab)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)


def turn_right(pas, pab):
    pA.start(pas)
    pB.start(pab)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)


def stop():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)


print("forward")
move_forward()
sleep(2)
stop()
print("backwards")
move_backward()
sleep(2)
stop()
print("left")
turn_left()
sleep(2)
stop()
print("right")
turn_right()
sleep(2)
stop()
GPIO.cleanup()
