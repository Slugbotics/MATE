#ifndef ESC_H
#define ESC_H
#include <Arduino.h>
#include <Servo.h>

//esc object functions
class EscControl {
  public:
    EscControl(int pin);
    void init();
    void updateEsc(int joystickValue);
    int getEscValue();

  //pin references
  private:
    Servo esc;
    int escPin;
    int escValue;
};

#endif