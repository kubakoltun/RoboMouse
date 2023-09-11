import RPi.GPIO as GPIO
import time

# there is an issue with the search of the longest path it gets stuck and just keeps spining to the left
# possibly because the distances where simular and too short
# stuck logic does not work every time (mainly when both sensors are completely covered up) 
# it may turn too gently which causes it to poke objects with its wheels

# SETUP
# Define the time threshold for stuck detection (in seconds)
stuck_start_time = 0
is_stuck = False
previous_distance = None
STUCK_THRESHOLD = 2

# Define distance thresholds for activating appropriate response speed
RAPID_TURN = 7
SLIGHT_TURN = 40
POSSIBLY_STUCK = 2
extensible_speed = 25

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

right_motor_speed = GPIO.PWM(ENA, 500)
right_motor_speed.start(0)
left_motor_speed = GPIO.PWM(ENB, 500)
left_motor_speed.start(0)
# SETUP


# MANEUVERS
def move_backward():
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)


def move_forward():
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)


def turn_left():
    GPIO.output(IN1A, GPIO.HIGH)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.HIGH)


def turn_right():
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.HIGH)
    GPIO.output(IN3B, GPIO.HIGH)
    GPIO.output(IN4B, GPIO.LOW)


def stop():
    GPIO.output(IN1A, GPIO.LOW)
    GPIO.output(IN2A, GPIO.LOW)
    GPIO.output(IN3B, GPIO.LOW)
    GPIO.output(IN4B, GPIO.LOW)
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

    if (pulse_start is None) or (pulse_start == 0):
        return 0

    if (pulse_end is None) or (pulse_end == 0):
        return 0

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
# DISTANCE MEASUREMENT


# MANEUVERS
def avoid_obstacle():
    move_backward()
    time.sleep(0.5)
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
    global is_stuck, stuck_start_time, previous_distance, extensible_speed

    extensible_speed = 75

    try:
        while True:
            # avoid_obstacle()
            print("LOOP STARTED")
            distance = distance_measurement()
            print("Distance {}, moving forward".format(distance))
            right_motor_speed.ChangeDutyCycle(extensible_speed)
            left_motor_speed.ChangeDutyCycle(extensible_speed)
            move_forward()

            if distance > SLIGHT_TURN:
                print("Can proceed current movement (distance > SLIGHT_TURN)")
                right_motor_speed.ChangeDutyCycle(extensible_speed)
                left_motor_speed.ChangeDutyCycle(extensible_speed)
                if extensible_speed < 100:
                    extensible_speed += 1
            elif RAPID_TURN < distance <= SLIGHT_TURN:
                # Begin turning slightly to the right
                print("Dropping down the speed and going right (RAPID_TURN < distance <= SLIGHT_TURN)")
                right_motor_speed.ChangeDutyCycle(extensible_speed)
                left_motor_speed.ChangeDutyCycle(extensible_speed+10)
                # I do not know where to turn best yet
            elif POSSIBLY_STUCK < distance <= RAPID_TURN:
                # Rapidly turn left
                print("Turning rapidly to the left")
                right_motor_speed.ChangeDutyCycle(extensible_speed+20)
                left_motor_speed.ChangeDutyCycle(extensible_speed)
                time.sleep(0.1)
            elif distance <= POSSIBLY_STUCK:
                right_motor_speed.ChangeDutyCycle(extensible_speed)
                left_motor_speed.ChangeDutyCycle(extensible_speed)
                avoid_obstacle()

            # # Check for stuck condition
            # if not is_stuck and distance <= SLIGHT_TURN:
            #     if previous_distance is None:
            #         previous_distance = distance
            #
            #     # Check if the distance is not changing significantly
            #     distance = distance_measurement()
            #     if abs(distance - previous_distance) < 2:
            #         if stuck_start_time == 0:
            #             print("Starting to count whether its stuck")
            #             stuck_start_time = time.time()
            #
            #         # Check if the robot is stuck for too long
            #         if time.time() - stuck_start_time > STUCK_THRESHOLD:
            #             print(f"Robot is stuck! {time.time} - {stuck_start_time} > {STUCK_THRESHOLD}")
            #             is_stuck = True
            #             # Recovery action
            #             print("Recover - back")
            #             move_backward()
            #             time.sleep(0.5)
            #
            #             # Turn left to attempt to get unstuck
            #             print("Recover - left")
            #             turn_left()
            #             time.sleep(0.1)
            #             stuck_start_time = 0
            #             is_stuck = False
            #     else:
            #         # Distance is changing, reset stuck variables
            #         is_stuck = False
            #         stuck_start_time = 0
            #         previous_distance = distance

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
# MOVEMENT
