// TODO - the stuck response is almost never called
// TODO - maybe a platform to simulate this code would be nice

// Sensor
int TRIG_PIN = 5;  
int ECHO_PIN = 6;  
int distanceInCm;        
long signalTime;     

// Right wheel
int ENA = 3;
int IN1A = 2;
int IN2A = 1;
// Left wheel
int IN3B = 13;
int IN4B = 12;
int ENB = 11;

// Natural movement parameters
int global_pwm_speed = 200;
int min_speed = 100;
int current_left_speed = global_pwm_speed;
int current_right_speed = global_pwm_speed;
const int RAPID_TURN = 30;
const int SLIGHT_TURN = 80;
const int SAFE_DISTANCE = 120;
const int POSSIBLY_STUCK = 6;
const int NUM_MEASUREMENTS = 9;

// Memory and randomness for naturalistic behavior
int last_avoid_direction = 0;  // 0: none, 1: left, 2: right
int consecutive_same_turns = 0;
int straight_line_counter = 0;
bool is_exploring = true;
unsigned long last_direction_change = 0;
unsigned long last_wiggle = 0;
int possibly_stuck_counter = 0;
 
void setup() {
    Serial.begin(9600);     
    // Sensor                   
    pinMode(TRIG_PIN, OUTPUT);                     
    pinMode(ECHO_PIN, INPUT);   

    // Motors
    pinMode(IN1A, OUTPUT);                     
    pinMode(IN2A, OUTPUT);                     
    pinMode(IN3B, OUTPUT); 
    pinMode(IN4B, OUTPUT); 
    
    // Initialize random seed from an unconnected analog pin
    randomSeed(analogRead(0));
}
  
void loop() {
    int distance = distance_measurement();
    // Reduced delay for more responsive movement
    delay(100);  
    
    // Check if possibly stuck
    if (distance <= POSSIBLY_STUCK) {
        handlePossiblyStuck();
    } 
    else {
        possibly_stuck_counter = 0;
    }
    
    // Normal navigation logic
    if (distance > SAFE_DISTANCE) {
        // Open space - occasionally make random movements for naturalistic exploration
        explore_mode(distance);
    } 
    else if (distance > SLIGHT_TURN) {
        // Path is clear but something is ahead - smooth approach
        approach_mode(distance);
    } 
    else if (RAPID_TURN < distance && distance <= SLIGHT_TURN) {
        // Getting close to obstacle - slow and adjust course
        caution_mode(distance);
    } 
    else if (distance <= RAPID_TURN) {
        // Obstacle near - avoid it
        avoid_obstacle();
    }
    
    // Add subtle speed variations for more natural movement
    addRandomWiggle();
}

void explore_mode(int distance) {
    // Free space behavior
    straight_line_counter++;
    
    // In open space, occasionally make random turns to mimic curiosity
    if (straight_line_counter > 20 || millis() - last_direction_change > 5000) {
        int random_choice = random(10);
        
        if (random_choice < 3) {  // 30% chance to slightly turn left
            current_left_speed = global_pwm_speed - random(20, 40);
            current_right_speed = global_pwm_speed;
        } 
        else if (random_choice < 6) {  // 30% chance to slightly turn right
            current_left_speed = global_pwm_speed;
            current_right_speed = global_pwm_speed - random(20, 40);
        } 
        else {  // 40% chance to go straight but maybe slightly uneven
            current_left_speed = global_pwm_speed - random(0, 15);
            current_right_speed = global_pwm_speed - random(0, 15);
        }
        
        last_direction_change = millis();
        straight_line_counter = 0;
    } 
    else {
        // Gradual transition to the target speeds for smooth movement
        smoothlyAdjustSpeeds(global_pwm_speed, global_pwm_speed, 10);
    }
    
    move_forward(current_left_speed, current_right_speed);
}

void approach_mode(int distance) {
    // Moderate distance - still safe to proceed but be aware
    int target_speed = map(distance, SLIGHT_TURN, SAFE_DISTANCE, min_speed + 30, global_pwm_speed);
    
    // Add slight curve sometimes like a cautious approach
    if (random(100) < 30) {  // 30% chance to curve slightly
        if (random(2) == 0) {
            smoothlyAdjustSpeeds(target_speed - 15, target_speed, 5);
        } 
        else {
            smoothlyAdjustSpeeds(target_speed, target_speed - 15, 5);
        }
    } 
    else {
        smoothlyAdjustSpeeds(target_speed, target_speed, 5);
    }
    
    move_forward(current_left_speed, current_right_speed);
}

void caution_mode(int distance) {
    // Near obstacle - slow down and adjust
    int target_speed = map(distance, RAPID_TURN, SLIGHT_TURN, min_speed, min_speed + 30);
    
    // Adaptive path selection - favor previously successful direction
    if (last_avoid_direction == 1) {  // Previously turned left
        smoothlyAdjustSpeeds(target_speed, target_speed + 25, 15);
    } 
    else if (last_avoid_direction == 2) {  // Previously turned right
        smoothlyAdjustSpeeds(target_speed + 25, target_speed, 15);
    } 
    else {
        // No previous direction - make a small, exploratory turn
        if (random(2) == 0) {
            smoothlyAdjustSpeeds(target_speed - 20, target_speed + 20, 15);
        } 
        else {
            smoothlyAdjustSpeeds(target_speed + 20, target_speed - 20, 15);
        }
    }
    
    move_forward(current_left_speed, current_right_speed);
}

void handlePossiblyStuck() {
    possibly_stuck_counter++;

    // Escalating response to being stuck
    if (possibly_stuck_counter >= 2) {
        int escape_strategy = random(3);
        
        if (escape_strategy == 0 || possibly_stuck_counter >= 5) {
            // Back up and turn sharply - for serious stuck situations
            stop();
            delay(200);
            move_backward(global_pwm_speed, global_pwm_speed);
            delay(500 + random(300));
            stop();
            delay(100);
            
            // Turn in opposite direction from last avoidance
            if (last_avoid_direction == 1) {
                turn_right(global_pwm_speed, global_pwm_speed);
            } 
            else {
                turn_left(global_pwm_speed, global_pwm_speed);
            }
            delay(400 + random(400));
            
            // Reset counter after dramatic action
            possibly_stuck_counter = 0;
        } 
        else if (escape_strategy == 1) {
            // Wiggle approach - small back and forth movements
            move_backward(global_pwm_speed, global_pwm_speed - 50);
            delay(200);
            move_forward(global_pwm_speed - 50, global_pwm_speed);
            delay(200);
            move_backward(global_pwm_speed - 50, global_pwm_speed);
            delay(200);
        } 
        else {
            // Pivot in place - rotate to find new direction without backing up
            if (random(2) == 0) {
                turn_left(global_pwm_speed, global_pwm_speed);
            } 
            else {
                turn_right(global_pwm_speed, global_pwm_speed);
            }
            delay(300 + random(300));
        }
        
        stop();
        delay(100);
    }
}

void smoothlyAdjustSpeeds(int targetLeft, int targetRight, int step) {
    // Gradually adjust current speeds toward target speeds for smooth transitions
    if (current_left_speed < targetLeft) {
        current_left_speed = min(current_left_speed + step, targetLeft);
    } 
    else if (current_left_speed > targetLeft) {
        current_left_speed = max(current_left_speed - step, targetLeft);
    }
    
    if (current_right_speed < targetRight) {
        current_right_speed = min(current_right_speed + step, targetRight);
    } 
    else if (current_right_speed > targetRight) {
        current_right_speed = max(current_right_speed - step, targetRight);
    }
}

void addRandomWiggle() {
    // Add subtle randomness to mimic natural imperfections in movement
    if (millis() - last_wiggle > 800) {  // Apply subtle changes every ~800ms
        int wiggle_amount = random(-10, 11);
        
        // Apply small random adjustment to wheels
        current_left_speed += wiggle_amount;
        current_right_speed -= wiggle_amount / 2;
        
        // Ensure speeds stay within reasonable range
        current_left_speed = constrain(current_left_speed, min_speed, global_pwm_speed);
        current_right_speed = constrain(current_right_speed, min_speed, global_pwm_speed);
        
        last_wiggle = millis();
    }
}

void avoid_obstacle() {
    stop();
    delay(100);

    // Improved obstacle avoidance with memory and learning
    int distances[NUM_MEASUREMENTS];
    int max_distance = 0;
    int max_index = 0;
    int sum_distances_left = 0;
    int sum_distances_right = 0;
    int count_left = 0;
    int count_right = 0;

    // Perform scanning with measurements
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        distances[i] = distance_measurement();
        delay(100);

        // Calculate statistics for decision making
        if (i < NUM_MEASUREMENTS / 2) {
            sum_distances_left += distances[i];
            count_left++;
        } 
        else {
            sum_distances_right += distances[i];
            count_right++;
        }

        if (distances[i] > max_distance) {
            max_distance = distances[i];
            max_index = i;
        }

        // Turn slightly for next measurement
        turn_left(global_pwm_speed - 20, global_pwm_speed - 20);
        delay(200);
        stop();
        delay(50);
    }

    // Bias decision based on previous success and current readings
    int avg_left = sum_distances_left / count_left;
    int avg_right = sum_distances_right / count_right;
    int prev_direction_bonus = 20;  // Bonus for previously successful direction
    
    // Decide which way to turn with slight memory bias
    bool turn_direction_left;
    
    if (last_avoid_direction == 1) {
        // Previously went left - bias toward left again
        turn_direction_left = (avg_left + prev_direction_bonus > avg_right);
    } 
    else if (last_avoid_direction == 2) {
        // Previously went right - bias toward right again
        turn_direction_left = (avg_left > avg_right + prev_direction_bonus);
    } 
    else {
        // No history - choose the better direction
        turn_direction_left = (avg_left > avg_right);
        
        // Sometimes add randomness for exploration
        if (abs(avg_left - avg_right) < 15 && random(100) < 40) {
            turn_direction_left = !turn_direction_left;
        }
    }

    // Execute the turn with natural acceleration/deceleration
    if (turn_direction_left) {
        // Record that we chose left
        last_avoid_direction = 1;
        
        // More natural gradual turning
        for (int speed = 100; speed <= global_pwm_speed; speed += 20) {
            turn_left(speed, speed);
            delay(50);
        }
        
        delay(600 + random(400));  // Randomized turn duration
        
        // Gradual deceleration from turn
        for (int speed = global_pwm_speed; speed >= 100; speed -= 20) {
            turn_left(speed, speed);
            delay(30);
        }
    } 
    else {
        // Record that we chose right
        last_avoid_direction = 2;
        
        // More natural gradual turning
        for (int speed = 100; speed <= global_pwm_speed; speed += 20) {
            turn_right(speed, speed);
            delay(50);
        }
        
        delay(600 + random(400));  // Randomized turn duration
        
        // Gradual deceleration from turn
        for (int speed = global_pwm_speed; speed >= 100; speed -= 20) {
            turn_right(speed, speed);
            delay(30);
        }
    }

    stop();
    delay(100);

    // Continue forward with slight turn in chosen direction
    if (turn_direction_left) {
        move_forward(global_pwm_speed - 30, global_pwm_speed);
    } else {
        move_forward(global_pwm_speed, global_pwm_speed - 30);
    }
    
    // Move forward briefly to clear the obstacle area
    delay(500 + random(200));
}

int distance_measurement() {
    digitalWrite(TRIG_PIN, LOW);        
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);       
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    digitalWrite(ECHO_PIN, HIGH); 
    signalTime = pulseIn(ECHO_PIN, HIGH);
    distanceInCm = signalTime / 58;    
  
    return distanceInCm;     
}

void move_forward(int speedA, int speedB) {
    analogWrite(ENA, speedA);
    analogWrite(ENB, speedB);
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
}

void move_backward(int speedA, int speedB) {
    analogWrite(ENA, speedA);
    analogWrite(ENB, speedB);
    digitalWrite(IN1A, HIGH);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, HIGH);
    digitalWrite(IN4B, LOW);
}

void turn_left(int speedA, int speedB) {
    analogWrite(ENA, speedA);
    analogWrite(ENB, speedB);
    digitalWrite(IN1A, HIGH);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
}

void turn_right(int speedA, int speedB) {
    analogWrite(ENA, speedA);
    analogWrite(ENB, speedB);
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
