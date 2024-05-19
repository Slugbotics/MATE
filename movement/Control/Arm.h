#include <Servo.h>

class ServoControl {
  private:
    int escPin;
    Servo servo;

  public:
    ServoControl(int pin);
    void init();
    void attach(int pin);
    void write(int angle);
    int read();
};



