import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# sensor
TRIG_RIGHT = 5
ECHO_RIGHT = 6

GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)
GPIO.output(TRIG_RIGHT, False)
time.sleep(0.1)
GPIO.output(TRIG_RIGHT, True)
time.sleep(0.0001)
GPIO.output(TRIG_RIGHT, False)

pulse_start = 0
pulse_end = 0

while GPIO.input(ECHO_RIGHT) == 0:
	pulse_start = time.time()
while GPIO.input(ECHO_RIGHT) == 1:
	pulse_end = time.time()

# if (pulse_start is None) or (pulse_start == 0):
# 	print(0)
#
# if (pulse_end is None) or (pulse_end == 0):
# 	print(0)

pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
print(distance)
# DISTANCE MEASUREMENT
