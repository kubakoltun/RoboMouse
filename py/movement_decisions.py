import RPi.GPIO as GPIO
import time

# right wheel
in1A = 25
in2A = 23
enA = 12
# left wheel
in3B = 17
in4B = 27
enB = 13
# sensor
trig_right = 5
echo_right = 6

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1A, GPIO.OUT)
GPIO.setup(in2A, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
# GPIO.output(in1A, GPIO.LOW)
# GPIO.output(in2A, GPIO.LOW)

GPIO.setup(in3B, GPIO.OUT)
GPIO.setup(in4B, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
# GPIO.output(in3B, GPIO.LOW)
# GPIO.output(in4B, GPIO.LOW)

pA = GPIO.PWM(enA, 500)
pA.start(75)
pB = GPIO.PWM(enB, 500)
pB.start(75)


def move_backward():
    # pA.start(pwm_speed)
    # pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    # GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    # GPIO.output(enB, GPIO.HIGH)
    # time.sleep(sleep)


def move_forward():
    # pA.start(pwm_speed)
    # pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    # GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    # GPIO.output(enB, GPIO.HIGH)
    # time.sleep(sleep)


def turn_left():
    # pA.start(pwm_speed)
    # pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    GPIO.output(enB, GPIO.HIGH)
    # time.sleep(sleep)


def turn_right():
    # pA.start(pwm_speed)
    # pB.start(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(enA, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    GPIO.output(enB, GPIO.HIGH)
    # time.sleep(sleep)


def stop():
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    # GPIO.output(enA, GPIO.Low)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)
    # GPIO.output(enB, GPIO.LOW)
    # time.sleep(sleep)


def distance_measurement():
    print("Setting up measurement...")
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
    return distance


# Define speed constants
forward_speed = 50
turning_speed = 50

# Define distance thresholds
min_distance = 10
max_distance = 20


def avoid_obstacle():
    # Stop the robot
    stop()
    time.sleep(0.1)

    # Measure distance after stopping
    distance = distance_measurement()
    print("Distance after stopping: {} cm".format(distance))

    # Turn right or left based on the measured distance
    if distance > max_distance:
        print("Turning right")
        turn_right()
    else:
        print("Turning left")
        turn_left()

    # Wait for a short duration before resuming forward movement
    time.sleep(0.5)


def main():
    try:
        while True:
            distance = distance_measurement()
            print("Distance: {} cm".format(distance))

            if distance > max_distance:
                # Move forward at full speed if there's no obstacle ahead
                pA.ChangeDutyCycle(forward_speed)
                pB.ChangeDutyCycle(forward_speed)
                move_forward()
            elif min_distance < distance <= max_distance:
                # Obstacle detected, initiate obstacle avoidance
                avoid_obstacle()
            else:
                # Obstacle too close, stop and wait
                stop()
                time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
