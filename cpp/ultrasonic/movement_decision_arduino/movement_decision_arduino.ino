// Pins
#define TRIG_PIN 5
#define ECHO_PIN 6
#define ENA 3
#define IN1A 2
#define IN2A 1
#define ENB 11
#define IN3B 13
#define IN4B 12

// Parameters
#define BASE_SPEED 180
#define TURN_SPEED 180
#define SAFE_DISTANCE 50
#define CRITICAL_DISTANCE 25
#define FULL_ROTATION_TIME 1266 // ms for 360 degrees
#define STUCK_DISTANCE_DELTA 2
#define STUCK_TIME 1200

// State machine
enum State {
    FORWARD,
    BACKUP,
    TURN,
    UNSTUCK
};
State state = FORWARD;
unsigned long stateStart = 0;

// Globals
int lastDistance = 0;
unsigned long stuckTimer = 0;
int turnDirection = 1; // left = 1, right = -1
int turnDegrees = 90;

void setup() {
    Serial.begin(9600);

    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    pinMode(IN1A, OUTPUT);
    pinMode(IN2A, OUTPUT);
    pinMode(IN3B, OUTPUT);
    pinMode(IN4B, OUTPUT);

    randomSeed(analogRead(A0));
}

void loop() {
    int distance = readDistance();

    // Stuck detection
    if (abs(distance - lastDistance) < STUCK_DISTANCE_DELTA) {
        if (millis() - stuckTimer > STUCK_TIME) {
            enterState(UNSTUCK);
        }
    } 
    else {
        stuckTimer = millis();
    }
    lastDistance = distance;

    // State machine
    switch (state) {
        case FORWARD:
            moveForward(BASE_SPEED);

            if (distance < CRITICAL_DISTANCE) {
                turnDirection = random(2) ? 1 : -1;
                enterState(BACKUP);
            }
            break;

        case BACKUP:
            moveBackward(BASE_SPEED);

            if (millis() - stateStart > 400) {
                turnDegrees = random(60, 140);
                enterState(TURN);
            }
            break;

        case TURN: {
            int turnTime = (turnDegrees * FULL_ROTATION_TIME) / 360;

            if (turnDirection == 1) {
                turnLeft(TURN_SPEED);
            }
            else {
                turnRight(TURN_SPEED);
            }

            if (millis() - stateStart > turnTime) {
                enterState(FORWARD);
            }
            break;
        }

        case UNSTUCK:
            moveBackward(BASE_SPEED);
            if (millis() - stateStart > 600) {
                turnDirection = random(2) ? 1 : -1;
                turnDegrees = random(120, 180);
                enterState(TURN);
            }
            break;
    }
}

// State handler
void enterState(State newState) {
    stopMotors();
    state = newState;
    stateStart = millis();
}

// Sensor
int readDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long signalTime = pulseIn(ECHO_PIN, HIGH, 25000);
    if (signalTime == 0) return 400;

    return signalTime / 58;
}

// MOTOR CONTROL
void moveForward(int speed) {
    analogWrite(ENA, speed);
    analogWrite(ENB, speed);
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
}

void moveBackward(int speed) {
    analogWrite(ENA, speed);
    analogWrite(ENB, speed);
    digitalWrite(IN1A, HIGH);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, HIGH);
    digitalWrite(IN4B, LOW);
}

void turnLeft(int speed) {
    analogWrite(ENA, speed);
    analogWrite(ENB, speed);
    digitalWrite(IN1A, HIGH);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, HIGH);
}

void turnRight(int speed) {
    analogWrite(ENA, speed);
    analogWrite(ENB, speed);
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, HIGH);
    digitalWrite(IN3B, HIGH);
    digitalWrite(IN4B, LOW);
}

void stopMotors() {
    digitalWrite(IN1A, LOW);
    digitalWrite(IN2A, LOW);
    digitalWrite(IN3B, LOW);
    digitalWrite(IN4B, LOW);
}
