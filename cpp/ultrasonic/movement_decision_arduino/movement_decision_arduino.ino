// sensor
int TRIG_PIN = 5;  
int ECHO_PIN = 6;  
int distanceInCm;        
long signalTime;     

// right wheel
int ENA = 3;
int IN1A = 2;
int IN2A = 1;
// left wheel
int IN3B = 13;
int IN4B = 12;
int ENB = 11;

// define thresholds
int global_pwm_speed = 200;
int extensible_speed = 65;
const int RAPID_TURN = 30;
const int SLIGHT_TURN = 80;
const int POSSIBLY_STUCK = 6;
const int NUM_MEASUREMENTS = 9;


int possibly_stuck_counter = 0;
 
void setup() {
  Serial.begin(9600);     
  // sensor                   
  pinMode(TRIG_PIN, OUTPUT);                     
  pinMode(ECHO_PIN, INPUT);   

  // motors
  pinMode(IN1A, OUTPUT);                     
  pinMode(IN2A, OUTPUT);                     
  pinMode(IN3B, OUTPUT); 
  pinMode(IN4B, OUTPUT); 
   
}
  
void loop() {
    int distance = distance_measurement();
    delay(200);

    // The path is free - i can gain speed
    if (distance > SLIGHT_TURN) {
      move_forward(global_pwm_speed, global_pwm_speed); 
    } 
    else if (RAPID_TURN < distance && distance <= SLIGHT_TURN) {
      // Slow down as it gets closer
      int slow_speed = map(distance, RAPID_TURN, SLIGHT_TURN, 100, global_pwm_speed);  
      move_forward(slow_speed, slow_speed + 10);
    } 
    else if (distance <= RAPID_TURN) {
      avoid_obstacle();  
    }

    // todo it does not react if the distance is the same for too long
    if (distance <= POSSIBLY_STUCK) {
      possibly_stuck_counter++;
      if (possibly_stuck_counter >= 4) {
        possibly_stuck_counter = 0;
        move_backward(global_pwm_speed, global_pwm_speed);
        delay(800);
        avoid_obstacle();
      }
    }
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

void avoid_obstacle() {
    stop();  

    int distances[NUM_MEASUREMENTS];
    int max_distance = 0;
    int max_index = 0;

    // Perform about 360-degree turn with measurements at each step
    for (int i = 0; i < NUM_MEASUREMENTS; i++) {
        // Measure the distance at current angle
        distances[i] = distance_measurement();  
        // Allow time for the sensor to stabilize
        delay(300);  

        // Record the best distance and its index
        if (distances[i] > max_distance) {
            max_distance = distances[i];
            max_index = i;
        }

        // Turn left slightly (40 degrees)
        turn_left(global_pwm_speed, global_pwm_speed);
        delay(250);  
        stop();
        delay(100);  
    }

    // Now, turn to face the direction with the maximum distance
    int angle_to_turn = max_index * 40; 

    // If the best path is to the left (less than 180 degrees), turn left
    if (angle_to_turn <= 180) {
        turn_left(global_pwm_speed, global_pwm_speed);
        // Map angle to time (adjust based on testing)
        delay(map(angle_to_turn, 0, 180, 0, 1500));  
    } 
    // If the best path is to the right (more than 180 degrees), turn right instead
    else {
        turn_right(global_pwm_speed, global_pwm_speed);
        // Turn right for the remaining angle
        delay(map(360 - angle_to_turn, 0, 180, 0, 1500));  
    }

    stop();  

    // Move forward after turning to the best direction
    move_forward(global_pwm_speed, global_pwm_speed);
    delay(500); 
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