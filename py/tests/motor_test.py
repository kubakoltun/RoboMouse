import RPi.GPIO as GPIO
import time

# right wheel
in1A = 25
in2A = 23
enA = 12
# left wheel
in3B = 17
in4B = 27
enB = 13


GPIO.setmode(GPIO.BCM)


GPIO.setup(in1A, GPIO.OUT)
GPIO.setup(in2A, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
#GPIO.output(in1A, GPIO.LOW)
#GPIO.output(in2A, GPIO.LOW)

GPIO.setup(in3B, GPIO.OUT)
GPIO.setup(in4B, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
#GPIO.output(in3B, GPIO.LOW)
#GPIO.output(in4B, GPIO.LOW)

pA = GPIO.PWM(enA, 500)
pA.start(75)
pB = GPIO.PWM(enB, 500)
pB.start(75)


def move_forward():
    #pA.start(pwm_speed)
    #pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    #GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    #GPIO.output(enB, GPIO.HIGH)
    #time.sleep(sleep)


def move_backward():
    #pA.start(pwm_speed)
    #pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    #GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    #GPIO.output(enB, GPIO.HIGH)
    #time.sleep(sleep)


def turn_left():
    #pA.start(pwm_speed)
    #pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    GPIO.output(enB, GPIO.HIGH)
    #time.sleep(sleep)


def turn_right():
    #pA.start(pwm_speed)
    #pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    GPIO.output(enB, GPIO.HIGH)
    #time.sleep(sleep)


def stop():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    #GPIO.output(enA, GPIO.Low)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)
    #GPIO.output(enB, GPIO.LOW)
    #time.sleep(sleep)


print("forward")
move_backward()
time.sleep(2)
stop()
print('break')
time.sleep(2)
print("backwards")
move_forward()
time.sleep(2)
stop()
print('break')
time.sleep(2)
print("left")
turn_left()
time.sleep(2)
stop()
print('break')
time.sleep(2)

print("right")
turn_right()
time.sleep(2)
stop()
print('break')
time.sleep(2)


GPIO.cleanup()
