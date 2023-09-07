import RPi.GPIO as GPIO
from distance_measurement import *
import time

def move_forward():
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)


def move_backward():
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)


def turn_left():
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)


def turn_right():
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)


def stop():
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.LOW)


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
