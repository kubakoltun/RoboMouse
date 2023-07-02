import RPi.GPIO as GPIO
from time import sleep

in1 = 24
in2 = 23
en = 25

in3 = 17
in4 = 27
enB = 22

temp1 = 1


GPIO.setmode(GPIO.BCM)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

p = GPIO.PWM(en, 1000)
p.start(50)
pB = GPIO.PWM(enB, 1000)
pB.start(50)


print("run")
GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.HIGH)
GPIO.output(in4, GPIO.LOW)
sleep(5)
print("ran")
GPIO.cleanup()

