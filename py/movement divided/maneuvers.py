import RPi.GPIO as GPIO
from distance_measurement import *
import time


def move_forward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)
    # time.sleep(sleep)


def move_backward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)
    # time.sleep(sleep)


def turn_left():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)
    # time.sleep(sleep)


def turn_right():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)
    # time.sleep(sleep)


def stop():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.LOW)
    # time.sleep(sleep)


def avoid_obstacle():
    direction = []
    for path in range(5):
        distance = distance_measurement()
        print("Distance: {} cm".format(distance))
        direction.append(distance)
        turn_left()
        time.sleep(0.1)

    max_distance_index = direction.index(max(direction))

    for longest_path in range(max_distance_index):
        turn_right()
        time.sleep(0.1)

    move_forward()
    time.sleep(0.5)
