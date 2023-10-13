#include <iostream>
#include <wiringPi.h>
#include <softPwm.h>
#include <thread>
#include <chrono>

// right wheel
#define IN1A 25
#define IN2A 23
#define ENA 12
// left wheel
#define IN3B 17
#define IN4B 27
#define ENB 13
// sensor
#define TRIG_RIGHT 5
#define ECHO_RIGHT 6

// SETUP
const int stuck_threshold = 2; 
int stuck_start_time = 0;
bool is_stuck = false;
float previous_distance = 0;
const int global_pwm_speed = 50;

// Define thresholds
const int RAPID_TURN = 20
const int SLIGHT_TURN = 50
const int POSSIBLY_STUCK = 6
const int extensible_speed = 65

// MANEUVERS
void move_forward() {
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
}

void move_backward() {
    digitalWrite(IN1A, HIGH);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, HIGH);
    digitalWrite(IN4B, LOW);
}

void turn_left() {
    digitalWrite(IN1A, HIGH);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
}

void turn_right() {
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3B, HIGH);
    digitalWrite(IN4B, LOW);
}

void stop() {
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, LOW);
}

float distance_measurement() {
    digitalWrite(TRIG_RIGHT, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_RIGHT, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_RIGHT, LOW);

    while (digitalRead(ECHO_RIGHT) == LOW);
    long startTime = micros();
    while (digitalRead(ECHO_RIGHT) == HIGH);
    long endTime = micros();
    long pulseDuration = endTime - startTime;
    float distance = pulseDuration / 58.0;
    return distance;
}


void avoid_obstacle() {
    move_backward();
    // Sleep for 0.3 seconds
    usleep(300000); 

    std::vector<double> direction;

    for (int path = 0; path < 4; path++) {
        softPwmWrite(ENA, 0);
        softPwmWrite(ENB, 0);
        double distance = distance_measurement();
        std::cout << "Distance: " << distance << " cm, from path: " << path << std::endl;
        direction.push_back(distance);
        turn_left();
        softPwmWrite(ENA, extensible_speed);
        softPwmWrite(ENB, extensible_speed);
        usleep(500000); 
    }

    int max_distance_position = std::distance(direction.begin(), std::max_element(direction.begin(), direction.end())) + 1;

    for (int longest_path = 0; longest_path < max_distance_position; longest_path++) {
        softPwmWrite(ENA, 0);
        softPwmWrite(ENB, 0);
        usleep(500000); 
        softPwmWrite(ENA, extensible_speed);
        softPwmWrite(ENB, extensible_speed);
        turn_left();
        usleep(500000); 
    }
}

int main() {
    wiringPiSetup();
    pinMode(IN1A, OUTPUT);
    pinMode(IN2A, OUTPUT);
    pinMode(ENA, OUTPUT);
    pinMode(IN3B, OUTPUT);
    pinMode(IN4B, OUTPUT);
    pinMode(ENB, OUTPUT);

    pinMode(TRIG_RIGHT, OUTPUT);
    pinMode(ECHO_RIGHT, INPUT);

    softPwmCreate(ENA, global_pwm_speed, 100);
    softPwmCreate(ENB, global_pwm_speed, 100);

    try {
        int has_been_avoided = -1;
        while (true) {
            has_been_avoided += 1;
            avoid_obstacle();
            float distance = distance_measurement();

            if (distance > SLIGHT_TURN) {
                softPwmWrite(ENA, extensible_speed);
                softPwmWrite(ENB, extensible_speed);
            }
            else if (RAPID_TURN < distance && distance <= SLIGHT_TURN) {
                // Begin turning slightly to the right
                std::cout << "Going RIGHT" << std::endl;
                softPwmWrite(ENA, extensible_speed);
                softPwmWrite(ENB, extensible_speed + 10);
                // I do not know where to turn best yet
            }
            else if (POSSIBLY_STUCK < distance && distance <= RAPID_TURN) {
                // Rapidly turn left
                std::cout << "Turning rapidly to the LEFT" << std::endl;
                softPwmWrite(ENA, extensible_speed + 20);
                softPwmWrite(ENB, extensible_speed);
                delay(100);
            }
            else if (has_been_avoided % 10 == 0) {
                // Assuming that the distance requires finding a new path
                has_been_avoided = 0;
                std::cout << "Look for a better PATH" << std::endl;
                softPwmWrite(ENA, extensible_speed);
                softPwmWrite(ENB, extensible_speed);
                avoid_obstacle();
            } else {
                softPwmWrite(ENA, extensible_speed);
                softPwmWrite(ENB, extensible_speed + 20);
                delay(100);
            }

            has_been_avoided++;
        }

    } catch (...) {
        std::cout << "Program terminated by the user." << std::endl;
    } finally {
        digitalWrite(IN1A, LOW);
        digitalWrite(IN2A, LOW);
        digitalWrite(IN3B, LOW);
        digitalWrite(IN4B, LOW);
        digitalWrite(ENA, LOW);
        digitalWrite(ENB, LOW);
    }

    return 0;
}
