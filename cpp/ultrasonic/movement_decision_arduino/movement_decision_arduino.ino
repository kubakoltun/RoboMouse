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

    // the path is free - i can gain speed
    if (distance > SLIGHT_TURN) {
      move_forward(global_pwm_speed, global_pwm_speed);
    } 
    // obsticle not so far away - performing a SLIGHT TURN
    else if (RAPID_TURN < distance && distance <= SLIGHT_TURN) {
      move_forward(global_pwm_speed, global_pwm_speed+10);
    } 
    // obsticle pretty close - prefoming a RAPID TURN
    else if (POSSIBLY_STUCK < distance && distance <= RAPID_TURN) {
      avoid_obstacle();
    } 
    // else {
    //   move_forward(global_pwm_speed-10, global_pwm_speed-10);
    //   delay(100);
    // }

    if (distance <= POSSIBLY_STUCK) {
      possibly_stuck_counter++;
      if (possibly_stuck_counter >= 4) {
        possibly_stuck_counter = 0;
        move_backward(global_pwm_speed, global_pwm_speed);
        delay(500);
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
  int max_distance_position = 1;
  int max_distance = distance_measurement();
  delay(200);

  for (int path = 2; path <= 4; path++) {
    // it makes a turn which is about 30 degrees
    turn_left(global_pwm_speed, global_pwm_speed);
    delay(100);
    stop();
    delay(200);
    int distance = distance_measurement();
    delay(200);

    if (distance > max_distance) {
      max_distance = distance;
      max_distance_position = path;
    }
  }

  if (max_distance_position != 4) {
    turn_left(global_pwm_speed, global_pwm_speed);
    delay(100*max_distance_position);
  }
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