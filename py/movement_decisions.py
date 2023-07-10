import RPi.GPIO as GPIO
import time


# right wheel
in1A = 24
in2A = 23
enA = 25
# left wheel
in3B = 17
in4B = 27
enB = 22
# first sensor
trig_right = 5
echo_right = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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
pA.start(25)
pB = GPIO.PWM(enB, 1000)
pB.start(25)


def distance_measurement():
    print("Setting up mesurement...")
    GPIO.setup(trig_right, GPIO.OUT)
    GPIO.setup(echo_right, GPIO.IN)
    GPIO.output(trig_right, False)
    print("Sensor settles")
    time.sleep(2)
    GPIO.output(trig_right, True)
    time.sleep(0.00001)
    GPIO.output(trig_right, False)

    while GPIO.input(echo_right) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_right) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance


def move_forward():
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)


def move_backward():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)


def turn_left():
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)


def turn_right():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)


def stop():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)


while True:
    distance = distance_measurement()
    print("Distance: {} cm".format(distance))

    if distance > 30:
        print("Moving forward")
        move_forward()
    else:
        print("Stopping")
        stop()
        time.sleep(1)

        print("Turning left")
        turn_left()
        time.sleep(2)

    time.sleep(0.1)


GPIO.cleanup()
