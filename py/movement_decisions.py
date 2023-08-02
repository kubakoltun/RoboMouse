import RPi.GPIO as GPIO
import time
import threading
# TODO speed does not change, I want to scale it (depending on the distance)
# TODO while stopping or detecting any change in movement lower the speed gradually
# TODO Improve recovery action - do not work at all
# TODO observe: wheels, measuring speed (is it enough), turning speed (does the 90 degree turn takes 0.25s at 50 pwm)
# TODO 0.25 makes about 2.5 rotations with speed of 50

# SETUP
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

GPIO.setup(in3B, GPIO.OUT)
GPIO.setup(in4B, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)


# Define speed variables
global_pwm_speed = 50

pA = GPIO.PWM(enA, 500)
pA.start(global_pwm_speed)
pB = GPIO.PWM(enB, 500)
pB.start(global_pwm_speed)
# SETUP


# MANEUVERS
def move_backward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    # time.sleep(sleep)


def move_forward():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    # time.sleep(sleep)


def turn_left():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.HIGH)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.HIGH)
    # time.sleep(sleep)


def turn_right():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.HIGH)
    GPIO.output(in3B, GPIO.HIGH)
    GPIO.output(in4B, GPIO.LOW)
    # time.sleep(sleep)


def stop():
    # pA.ChangeDutyCycle(pwm_speed)
    # pB.ChangeDutyCycle(pwm_speed)
    GPIO.output(in1A, GPIO.LOW)
    GPIO.output(in2A, GPIO.LOW)
    GPIO.output(in3B, GPIO.LOW)
    GPIO.output(in4B, GPIO.LOW)
    # time.sleep(sleep)
# MANEUVERS


# SETUP
# Define distance thresholds
min_distance = 7
max_distance = 20
# SETUP


# DISTANCE MEASUREMENT
def distance_measurement():
    GPIO.setup(trig_right, GPIO.OUT)
    GPIO.setup(echo_right, GPIO.IN)
    GPIO.output(trig_right, False)
    time.sleep(1)
    GPIO.output(trig_right, True)
    time.sleep(0.0001)
    GPIO.output(trig_right, False)

    

    pulse_start = 0;
    pulse_end = 0;
    
    while GPIO.input(echo_right) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_right) == 1:
        pulse_end = time.time()
        
        
    #pulse_start = GPIO.wait_for_edge(echo_right, GPIO.RISING, timeout=1000)
    if pulse_start is None:
        return float('inf')  

    #pulse_end = GPIO.wait_for_edge(echo_right, GPIO.FALLING, timeout=1000)
    if pulse_end is None:
        return float('inf')  
	

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance
# DISTANCE MEASUREMENT


# MANEUVERS
def avoid_obstacle():
    stop()

    # Measure distance after stopping
    distance = distance_measurement()
    print("Distance after stopping: {} cm".format(distance))

    if distance > min_distance:
        # Perform the initial right turn
        print("Turning right")
        turn_right()
        # Wait for the robot to complete the turn - need to monitor how long does it take
        time.sleep(0.25)

        # Measure distance to the right after turning
        right_distance = distance_measurement()
        print("Distance to the right after turning: {} cm".format(right_distance))

        # if right_distance > min_distance:
        #     # Turn right again to avoid the obstacle
        #     print("Turning right again")
        #     turn_right()
        if right_distance < min_distance:
            # Not enough space on the right, perform a 180-degree turn to the left
            print("Performing a 180-degree turn to the left")
            turn_left()
            time.sleep(0.5)

            # Check the distance after the 180-degree turn
            right_distance = distance_measurement()
            print("Distance after 180-degree turn: {} cm".format(right_distance))

            if right_distance <= min_distance:
                # There's still an obstacle on both sides, turn left again to avoid it
                print("Turning left again to avoid the obstacle")
                turn_left()
                time.sleep(0.25)

    # Wait for a short duration before resuming forward movement
    time.sleep(0.5)
# MANEUVERS


# SETUP
# Define the time threshold for stuck detection (in seconds)
stuck_threshold = 5
stuck_start_time = 0
is_stuck = False
# SETUP


# MOVEMENT
def main():
    global is_stuck, stuck_start_time

    try:
        #threading.Thread(target=distance_monitoring_thread, daemon=True).start()

        while True:
            distance = distance_measurement()
            print("Distance: {} cm".format(distance))

            # Check if the robot is stuck
            if distance > max_distance:
                # The robot is moving forward
                is_stuck = False
                stuck_start_time = 0
                # Still need to implement a logic for scaling the speed
                pA.ChangeDutyCycle(global_pwm_speed)
                pB.ChangeDutyCycle(global_pwm_speed)
                move_forward()
            elif min_distance < distance <= max_distance:
                # Obstacle detected, initiate obstacle avoidance
                is_stuck = False
                stuck_start_time = 0
                avoid_obstacle()
            else:
                # Obstacle too close, stop and wait
                is_stuck = False
                stuck_start_time = 0
                stop()
                time.sleep(0.1)

            # Check for stuck condition
            if not is_stuck and distance <= max_distance:
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
                    time.sleep(0.25)

            # Continuous monitoring of distance - will it
            #distance_monitoring_thread()
            #time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()
# MOVEMENT


# DISTANCE MEASUREMENT
#def distance_monitoring_thread():
 #   while True:
  #      distance = distance_measurement()
   #     print("Distance: {} cm".format(distance))
    #    time.sleep(0.1)
# DISTANCE MEASUREMENT


# MOVEMENT
if __name__ == "__main__":
    main()
# MOVEMENT
