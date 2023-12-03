#ifndef ESC_H
#define ESC_H
#include <Arduino.h>
#include <Servo.h>

class EscControl {
  public:
    EscControl(int pin);
    void init();
    void updateEsc(int joystickValue);
    int getEscValue();

  private:
    Servo esc;
    int escPin;
    int escValue;
};

#endif