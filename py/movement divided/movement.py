import RPi.GPIO as GPIO
from maneuvers import *

def main():
    global is_stuck, stuck_start_time, previous_distance

    try:
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
                        time.sleep(0.25)

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
