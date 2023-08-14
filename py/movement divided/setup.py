import RPi.GPIO as GPIO


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


# Define the time threshold for stuck detection (in seconds)
stuck_threshold = 2
stuck_start_time = 0
is_stuck = False
previous_distance = None

# Define distance thresholds
min_distance = 7
max_distance = 20

