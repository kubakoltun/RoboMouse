import RPi.GPIO as GPIO


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


# Define distance thresholds
min_distance = 7
max_distance = 20


# Define the time threshold for stuck detection (in seconds)
stuck_threshold = 5
stuck_start_time = 0
is_stuck = False

