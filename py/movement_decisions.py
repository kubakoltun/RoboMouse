import RPi.GPIO as GPIO
import time
import threading

# better logic for getting stuck - current does not work in any way

# SETUP
# Define the time threshold for stuck detection (in seconds)
stuck_start_time = 0
is_stuck = False
previous_distance = None

# Define thresholds
MIN_DISTANCE = 7
MAX_DISTANCE = 20
STUCK_THRESHOLD = 2

# right wheel
IN1A = 25
IN2A = 23
ENA = 12
# left wheel
IN3B = 17
IN4B = 27
ENB = 13
# sensor
TRIG_RIGHT = 5
ECHO_RIGHT = 6

GPIO.setmode(GPIO.BCM)
# right wheel setup
GPIO.setup(IN1A, GPIO.OUT)
GPIO.setup(IN2A, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
# left wheel setup
GPIO.setup(IN3B, GPIO.OUT)
GPIO.setup(IN4B, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# define speed variable
global_pwm_speed = 50

pA = GPIO.PWM(ENA, 500)
pA.start(global_pwm_speed)
pB = GPIO.PWM(ENB, 500)
pB.start(global_pwm_speed)
# SETUP


# MANEUVERS
def move_forward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)
    # time.sleep(sleep)


def move_backward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)
    # time.sleep(sleep)


def turn_left():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)
    # time.sleep(sleep)


def turn_right():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)
    # time.sleep(sleep)


def stop():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.LOW)
    # time.sleep(sleep)
# MANEUVERS


# DISTANCE MEASUREMENT
def distance_measurement():
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

    # pulse_start = GPIO.wait_for_edge(echo_right, GPIO.RISING, timeout=1000)
    if (pulse_start is None) or (pulse_start == 0):
        return 0

        # pulse_end = GPIO.wait_for_edge(echo_right, GPIO.FALLING, timeout=1000)
    if (pulse_end is None) or (pulse_end == 0):
        return 0

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
# DISTANCE MEASUREMENT


# MANEUVERS
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
# MANEUVERS


# MOVEMENT
def main():
    global is_stuck, stuck_start_time, previous_distance

    try:
        # threading.Thread(target=distance_monitoring_thread, daemon=True).start()

        while True:
            avoid_obstacle()
            distance = distance_measurement()
            if distance > max_distance:
                # The robot is moving forward
                is_stuck = False
                # stuck_start_time = 0
                # Still need to implement a logic for scaling the speed
                # pA.ChangeDutyCycle(global_pwm_speed)
                # pB.ChangeDutyCycle(global_pwm_speed)
                move_forward()
            elif min_distance < distance <= max_distance:
                # Obstacle detected, initiate obstacle avoidance
                is_stuck = False
                # stuck_start_time = 0
                avoid_obstacle()
            else:
                # Obstacle too close, stop and wait
                is_stuck = False
                # stuck_start_time = 0
                stop()
                time.sleep(0.1)

            # Check for stuck condition
            if not is_stuck and distance <= max_distance:
                if previous_distance is None:
                    previous_distance = distance

                # Check if the distance is not changing significantly
                distance = distance_measurement()
                if abs(distance - previous_distance) < 2:  # Adjust the threshold as needed
                    if stuck_start_time == 0:
                        stuck_start_time = time.time()

                    # Check if the robot is stuck for too long
                    if time.time() - stuck_start_time > stuck_threshold:
                        print("Robot is stuck!")
                        is_stuck = True
                        # Recovery action
                        move_backward()
                        time.sleep(0.5)

                        # Turn left to attempt to get unstuck
                        turn_left()
                        time.sleep(0.1)
                        stuck_start_time = 0
                        is_stuck = False
                else:
                    # Distance is changing, reset stuck variables
                    is_stuck = False
                    stuck_start_time = 0
                    previous_distance = distance

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()
        

if __name__ == "__main__":
    main()
# MOVEMENT
