#include <NewPing.h>
#include <AFMotor.h>

// sensore
#define TRIG_PIN 5
#define ECHO_PIN 6

// right wheel
#define ENA 12
#define IN1A 25
#define IN2A 23
// left wheel
#define IN3B 17
#define IN4B 27
#define ENB 13

#define RAPID_TURN 20
#define SLIGHT_TURN 50
#define POSSIBLY_STUCK 6
#define extensible_speed 65
#define global_pwm_speed 50

NewPing sonar(TRIG_PIN, ECHO_PIN);
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);

void setup() {
  motor1.setSpeed(0); 
  motor2.setSpeed(0);
  motor1.run(RELEASE); 
  motor2.run(RELEASE);
  Serial.begin(9600);
}

void move_forward() {
  motor1.setSpeed(global_pwm_speed);
  motor2.setSpeed(global_pwm_speed);
  motor1.run(FORWARD);
  motor2.run(FORWARD);
}

void move_backward() {
  motor1.setSpeed(global_pwm_speed);
  motor2.setSpeed(global_pwm_speed);
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
}

void turn_left() {
  motor1.setSpeed(global_pwm_speed);
  motor2.setSpeed(global_pwm_speed);
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
}

// arg
void turn_right() {
  motor1.setSpeed(global_pwm_speed);
  motor2.setSpeed(global_pwm_speed);
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
}

void stop() {
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}

void avoid_obstacle() {
  move_backward();
  delay(300);

  int max_distance_position = 1;
  float max_distance = sonar.ping_cm();

  for (int path = 2; path <= 4; path++) {
    turn_left();
    delay(500);
    move_forward();
    delay(500);
    float distance = sonar.ping_cm();

    if (distance > max_distance) {
      max_distance = distance;
      max_distance_position = path;
    }
  }

  for (int longest_path = 1; longest_path < max_distance_position; longest_path++) {
    turn_left();
    delay(500);
  }
}

void loop() {
  int has_been_avoided = -1;

  while (true) {
    has_been_avoided += 1;
    avoid_obstacle();
    float distance = sonar.ping_cm();

    if (distance > SLIGHT_TURN) {
      motor1.setSpeed(extensible_speed);
      motor2.setSpeed(extensible_speed);
      move_forward();
    } 
    else if (RAPID_TURN < distance && distance <= SLIGHT_TURN) {
      // Begin turning slightly to the right
      motor1.setSpeed(extensible_speed);
      motor2.setSpeed(extensible_speed + 10);
      turn_right();
    } 
    else if (POSSIBLY_STUCK < distance && distance <= RAPID_TURN) {
      // Rapidly turn left
      motor1.setSpeed(extensible_speed + 20);
      motor2.setSpeed(extensible_speed);
      delay(100);
    } 
    else if (has_been_avoided % 10 == 0) {
      // Assuming that the distance requires finding a new path
      has_been_avoided = 0;
      avoid_obstacle();
    } else {
      motor1.setSpeed(extensible_speed);
      motor2.setSpeed(extensible_speed + 20);
      delay(100);
    }

    has_been_avoided++;
  }
}
