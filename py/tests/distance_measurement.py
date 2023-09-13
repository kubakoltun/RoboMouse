import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig_right = 5
echo_right = 6


print("Distance mesurement is in progress...")
GPIO.setup(trig_right, GPIO.OUT)
GPIO.setup(echo_right, GPIO.IN)
GPIO.output(trig_right, False)
print("Sensor settles")
time.sleep(2)
GPIO.output(trig_right, True)
time.sleep(0.00001)
GPIO.output(trig_right, False)

pulse_start = 0
pulse_end = 0

while GPIO.input(echo_right) == 0:
	pulse_start = time.time()
while GPIO.input(echo_right) == 1:
	pulse_end = time.time()
	
	
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)


print("Distance: ", distance, " cm")
