import RPi.GPIO as GPIO
import time 


GPIO.setmode(gpio.BCM)
GPIO.setwarnings(False)
TRIGEVEN = 29;
ECHOEVEN = 31;
TRIGODD = 33;
ECHOODD = 35;
print("Distance mesurement is in progress...")
GPIO.setup(TRIGEVEN, GPIO.OUT)
GPIO.setup(ECHOEVEN, GPIO.IN)
GPIO.output(TRIGEVEN, False)
print("Sensor settles")
time.sleep(2)
GPIO.output(TRIGEVEN, True)
time.sleep(0.00001)
GPIO.output(TRIGEVEN, False)
while GPIO.input(ECHOEVEN) == 0:
	pulse_start = time.time()
while GPIO.input(ECHOEVEN) == 1:
	pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
print("Distance: ",discance," cm")
