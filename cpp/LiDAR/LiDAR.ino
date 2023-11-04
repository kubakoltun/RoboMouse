// LD19 PWM_FREQ MIN:20kHz TYP:30kHz 50kHz
// PWM 0% 40% 100% 40%=10HZ
// LD19: 230400
// STL27L:921600  40%PWM=10HZ

// 0: stop      - PWM: - 
// 1: normal    - PWM: 40%
// 2: slow      - PWM: 10%
// 3: fast      - PWM:100%
int modeSelect = 1;

bool wireInput12 = true;

#define SWITCH_PIN 0
// #define LD19_PIN   13
// #define LD14_PIN   14

#define START_PIN  12
#define PWM_PIN  3

#define SLOW_PWM    100
#define NORMAL_PWM  409
#define FAST_PWM    1023


void setup() {
  pinMode(SWITCH_PIN,INPUT);

  pinMode(START_PIN,OUTPUT); // ctrl the power switch.
  pinMode(PWM_PIN,OUTPUT);   // ctrl the PWM.

  digitalWrite(START_PIN, HIGH);

  Serial.begin(921600);

  analogWriteFreq(30000);
  analogWriteRange(1023);

  analogWrite(PWM_PIN, 409);
}


void switchCheck(){
  if(digitalRead(SWITCH_PIN) == LOW){
    digitalWrite(START_PIN, LOW);
    wireInput12 = false;
  }
  else{
    digitalWrite(START_PIN, HIGH);
    wireInput12 = true;
  }
}


void loop() {
  // switchCheck();

  if (Serial.available() > 0) {
    char state = Serial.read();
    if (state == '0') {
      modeSelect = 0;
      Serial.println("shut down");
    }
    else if (state == '1') {
      modeSelect = 1;
      Serial.println("normal speed");
    }
    else if (state == '2') {
      modeSelect = 2;
      Serial.println("slow speed");
    }
    else if (state == '3') {
      modeSelect = 3;
      Serial.println("fast speed");
    }
  }

  if(wireInput12 == false || modeSelect == 0){
    digitalWrite(START_PIN, LOW);
    digitalWrite(PWM_PIN, LOW);
    Serial.println("CASE 1");
  }
  else if(wireInput12 == true && modeSelect == 1){
    digitalWrite(START_PIN, HIGH);
    digitalWrite(PWM_PIN, NORMAL_PWM);
    Serial.println("CASE 2");
  }
  else if(wireInput12 == true && modeSelect == 2){
    digitalWrite(START_PIN, HIGH);
    digitalWrite(PWM_PIN, SLOW_PWM);
    Serial.println("CASE 3");
  }
  else if(wireInput12 == true && modeSelect == 3){
    digitalWrite(START_PIN, HIGH);
    digitalWrite(PWM_PIN, FAST_PWM);
    Serial.println("CASE 4");
  }

  delay(1000);

  // --- --- ---

  // put your main code here, to run repeatedly:
  // if(WIRE_CTRL == 1){
  //   switchCheck();
  // }
  
  // speedCheck();

  // if (Serial.available() > 0) {
  //   char state = Serial.read();
  //   if (state == '1') {
  //     digitalWrite(START_PIN, HIGH);
  //     WIRE_CTRL = 0;
  //   }
  //   else if (state == '0') {
  //     digitalWrite(START_PIN, LOW);
  //     WIRE_CTRL = 0;
  //   }
  //   else if (state == '2') {
  //     WIRE_CTRL = 1;
  //   }
  // }
}
