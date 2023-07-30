import RPi.GPIO as GPIO
from distance_measurement import *
import time


def move_backward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    # time.sleep(sleep)


def move_forward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    # time.sleep(sleep)


def turn_left():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    # time.sleep(sleep)


def turn_right():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    # time.sleep(sleep)


def stop():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)
    # time.sleep(sleep)


def avoid_obstacle():
    stop()

    # Measure distance after stopping
    distance = distance_measurement()
    print("Distance after stopping: {} cm".format(distance))

    if distance > min_distance:
        # Perform the initial right turn
        print("Turning right")
        turn_right()
        # Wait for the robot to complete the turn - need to monitor how long does it take
        time.sleep(0.25)

        # Measure distance to the right after turning
        right_distance = distance_measurement()
        print("Distance to the right after turning: {} cm".format(right_distance))

        # if right_distance > min_distance:
        #     # Turn right again to avoid the obstacle
        #     print("Turning right again")
        #     turn_right()
        if right_distance < min_distance:
            # Not enough space on the right, perform a 180-degree turn to the left
            print("Performing a 180-degree turn to the left")
            turn_left()
            time.sleep(0.5)

            # Check the distance after the 180-degree turn
            right_distance = distance_measurement()
            print("Distance after 180-degree turn: {} cm".format(right_distance))

            if right_distance <= min_distance:
                # There's still an obstacle on both sides, turn left again to avoid it
                print("Turning left again to avoid the obstacle")
                turn_left()
                time.sleep(0.25)

    # Wait for a short duration before resuming forward movement
    time.sleep(0.5)
