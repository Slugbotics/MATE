// EscControl.cpp

#include "ESC.h"

EscControl::EscControl(int pin) : escPin(pin) {}

//setup function
void EscControl::init() {
  esc.attach(escPin);
  esc.writeMicroseconds(1500);
}

//write esc values
void EscControl::updateEsc(int joystickValue) {
  escValue = map(joystickValue, -100, 100, 1100, 1900);//0 is 1500 for stop
  esc.writeMicroseconds(escValue);//write value
}

//get thruster values
int EscControl::getEscValue(){
  return escValue;
}
