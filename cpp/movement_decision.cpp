#include <iostream>
#include <wiringPi.h>
#include <softPwm.h>
#include <thread>
#include <chrono>

// SETUP
const int stuck_threshold = 2; // in seconds
unsigned int stuck_start_time = 0;
bool is_stuck = false;
float previous_distance = 0;

// Define thresholds
const int MIN_DISTANCE = 7;
const int MAX_DISTANCE = 20;

// right wheel
const int IN1A = 25;
const int IN2A = 23;
const int ENA = 12;
// left wheel
const int IN3B = 17;
const int IN4B = 27;
const int ENB = 13;
// sensor
const int TRIG_RIGHT = 5;
const int ECHO_RIGHT = 6;

// define speed variable
const int global_pwm_speed = 50;

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
    float direction[5];
    for (int path = 0; path < 5; path++) {
        float distance = distance_measurement();
        std::cout << "Distance: " << distance << " cm" << std::endl;
        direction[path] = distance;
        turn_left();
        delay(100);
    }

    int max_distance_index = 0;
    for (int i = 1; i < 5; i++) {
        if (direction[i] > direction[max_distance_index]) {
            max_distance_index = i;
        }
    }

    for (int longest_path = 0; longest_path < max_distance_index; longest_path++) {
        turn_right();
        delay(100);
    }

    move_forward();
    delay(500);
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
        while (true) {
            avoid_obstacle();
            float distance = distance_measurement();
            if (distance > MAX_DISTANCE) {
                is_stuck = false;
                move_forward();
            } else if (MIN_DISTANCE < distance && distance <= MAX_DISTANCE) {
                is_stuck = false;
                avoid_obstacle();
            } else {
                is_stuck = false;
                stop();
                delay(100);
            }

            if (!is_stuck && distance <= MAX_DISTANCE) {
                if (previous_distance == 0) {
                    previous_distance = distance;
                }

                distance = distance_measurement();
                if (abs(distance - previous_distance) < 2) {
                    if (stuck_start_time == 0) {
                        stuck_start_time = time(NULL);
                    }

                    if (time(NULL) - stuck_start_time > stuck_threshold) {
                        std::cout << "Robot is stuck!" << std::endl;
                        is_stuck = true;
                        move_backward();
                        delay(500);
                        turn_left();
                        delay(100);
                        stuck_start_time = 0;
                        is_stuck = false;
                    }
                } else {
                    is_stuck = false;
                    stuck_start_time = 0;
                    previous_distance = distance;
                }
            }
        }
    } catch (...) {
        std::cout << "Program terminated by user." << std::endl;
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