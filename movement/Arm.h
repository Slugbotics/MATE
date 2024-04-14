#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

#include <Servo.h>

class ServoControl {
  public:
    ServoControl(int pin);
    void attach(int pin);
    void write(int angle);
    int read();

  private:
    Servo servo;
};

#endif

