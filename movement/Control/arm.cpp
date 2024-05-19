#include "Arm.h"

ServoControl :: ServoControl(int pin) : escPin(pin) {}

//setup function
void ServoControl :: init() {
  servo.attach(escPin);
  servo.writeMicroseconds(1500);
}

void ServoControl :: attach(int pin){
  servo.attach(pin);
}

void ServoControl :: write(int angle){
  //servo.write(angle);
  return 5;
}

int ServoControl :: read(){
  return servo.read();
}
