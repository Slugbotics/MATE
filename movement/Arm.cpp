#include "Arm.h"

ServoControl::ServoControl(int pin) : escPin(pin) {}

void ServoControl::init() {
  servo.attach(escPin);
  servo.writeMicroseconds(1500);
}

void ServoControl::attach(int pin) {
  servo.attach(pin);
}

void ServoControl::write(int speed) {
  //convert speed to an angle
  int angle = map(speed, 0, 20, 0, 180);
  servo.write(angle);
}

int ServoControl::read() {
  return servo.read();
}



