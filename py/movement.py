import RPi.GPIO as GPIO
import threading
from maneuvers import *

# does not measure sufficient enough, gets stuck after a second, 5 large incorrect measurements per 50 total

def main():
    global is_stuck, stuck_start_time

    try:
        threading.Thread(target=distance_monitoring_thread, daemon=True).start()

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
            distance_monitoring_thread()

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
