import RPi.GPIO as GPIO
import time
from setup import *


def distance_measurement():
    GPIO.setup(trig_right, GPIO.OUT)
    GPIO.setup(echo_right, GPIO.IN)
    GPIO.output(trig_right, False)
    time.sleep(0.00001)
    GPIO.output(trig_right, True)
    time.sleep(0.00001)
    GPIO.output(trig_right, False)

    pulse_start = GPIO.wait_for_edge(echo_right, GPIO.RISING, timeout=500)
    if pulse_start is None:
        return float('inf')

    pulse_end = GPIO.wait_for_edge(echo_right, GPIO.FALLING, timeout=500)
    if pulse_end is None:
        return float('inf')

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance


def distance_monitoring_thread():
    while True:
        distance = distance_measurement()
        print("Distance: {} cm".format(distance))
        time.sleep(0.1)
