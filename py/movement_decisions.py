import RPi.GPIO as GPIO
import time


# right wheel
in1A = 24
in2A = 23
enA = 12
# left wheel
in3B = 17
in4B = 27
enB = 13
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

pA = GPIO.PWM(enA, 500)
pA.start(75)
pB = GPIO.PWM(enB, 500)
pB.start(75)


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


def move_forward(how_long):
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    time.sleep(how_long)


def move_backward(how_long):
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    time.sleep(how_long)


def turn_left(how_long):
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    time.sleep(how_long)


def turn_right(how_long):
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    time.sleep(how_long)


def stop(how_long):
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)
    time.sleep(how_long)


while True:
    distance = distance_measurement()
    print("Distance: {} cm".format(distance))

    if distance > 30:
        print("Moving forward")
        move_forward(40)
    else:
        print("Stopping")
        stop(1)

        print("Turning left")
        turn_left(2)

    time.sleep(0.1)


GPIO.cleanup()
