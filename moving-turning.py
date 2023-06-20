import RPi.GPIO as GPIO
import time


# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the wheels
left_wheel_pin1 = 17
left_wheel_pin2 = 18
right_wheel_pin1 = 27
right_wheel_pin2 = 22

# Set the GPIO pins as output
GPIO.setup(left_wheel_pin1, GPIO.OUT)
GPIO.setup(left_wheel_pin2, GPIO.OUT)
GPIO.setup(right_wheel_pin1, GPIO.OUT)
GPIO.setup(right_wheel_pin2, GPIO.OUT)

# Function to move forward
def move_forward():
    GPIO.output(left_wheel_pin1, GPIO.HIGH)
    GPIO.output(left_wheel_pin2, GPIO.LOW)
    GPIO.output(right_wheel_pin1, GPIO.HIGH)
    GPIO.output(right_wheel_pin2, GPIO.LOW)

# Function to move backward
def move_backward():
    GPIO.output(left_wheel_pin1, GPIO.LOW)
    GPIO.output(left_wheel_pin2, GPIO.HIGH)
    GPIO.output(right_wheel_pin1, GPIO.LOW)
    GPIO.output(right_wheel_pin2, GPIO.HIGH)

# Function to make a left turn
def turn_left():
    GPIO.output(left_wheel_pin1, GPIO.LOW)
    GPIO.output(left_wheel_pin2, GPIO.HIGH)
    GPIO.output(right_wheel_pin1, GPIO.HIGH)
    GPIO.output(right_wheel_pin2, GPIO.LOW)

# Function to make a right turn
def turn_right():
    GPIO.output(left_wheel_pin1, GPIO.HIGH)
    GPIO.output(left_wheel_pin2, GPIO.LOW)
    GPIO.output(right_wheel_pin1, GPIO.LOW)
    GPIO.output(right_wheel_pin2, GPIO.HIGH)

# Function to stop
def stop():
    GPIO.output(left_wheel_pin1, GPIO.LOW)
    GPIO.output(left_wheel_pin2, GPIO.LOW)
    GPIO.output(right_wheel_pin1, GPIO.LOW)
    GPIO.output(right_wheel_pin2, GPIO.LOW)

# Example usage
move_forward()
time.sleep(2)  # Move forward for 2 seconds
stop()
time.sleep(1)  # Stop for 1 second
turn_left()
time.sleep(1)  # Turn left for 1 second
stop()
time.sleep(1)  # Stop for 1 second
turn_right()
time.sleep(1)  # Turn right for 1 second
stop()
time.sleep(1)  # Stop for 1 second
move_backward()
time.sleep(2)  # Move backward for 2 seconds
stop()

# Cleanup GPIO pins
GPIO.cleanup()
