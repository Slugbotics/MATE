//use arduino's built in testing framework
#include <ArduinoUnit.h>
//pin references
int EscPin = 9;
int EscValue = 50;
//for esc functions
#include "ESC.h"
//test the esc setup
test(ESCControlInitialization) {
  //create esc control object with pin
  EscControl thrusterControl(EscPin);
  //check it is set to zero at initialization
  assertEqual(thrusterControl.getEscValue(), 0);
}
//test esc value range
test(UpdateESCWithValidValue) {
  //create esc control object with pin
  EscControl thrusterControl(EscPin);
  //update the esc alue with new esc value
  thrusterControl.updateEsc(EscValue);
  //check if the updated value matches
  assertEqual(thrusterControl.getEscValue(), EscValue);
}
//NOT YET IMPLEMENTED
//test reverse thrust

//test valid wire input

//test invalid wire input

//runt the test
void setup() {
  //run the test 
  Test::run();
}

