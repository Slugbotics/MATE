#include "Arm.h"

double scalar = 1.41732;

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
  servo.write((int)round(angle * scalar));
}

int ServoControl :: read(){
  return servo.read();
}
