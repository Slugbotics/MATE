#include "arm.h"

ServoControl :: ServoControl(int pin) : escPin(pin) {}

//setup function
void ServoControl :: init(): {
  servo.attach(escPin);
  servo.writeMicroseconds(1500);
}

void ServoControl :: attach(int pin){
  servo.attach(pin);
}

void ServoConrol :: write(int angle){
  servo.write(angle);
}

int ServoControl :: read(){
  return servo.read();
}
