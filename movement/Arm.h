#include <Servo.h>

class ServoControl {
  private:
    int escPin;
    Servo servo;
    bool isOpen;
    bool isClose;
    bool isRLSpin;
    bool isRBSpin;
    bool isSTR;

  public:
    ServoControl(int pin);
    void init();
    void attach(int pin);
    void writeHorizontal(int angle);
    void writeVertical(int angle);
    void setAction(bool open, bool close, bool rlspin, bool rbspin, bool str);
    int read();
};



