#ifndef BNO055_IMU_H
#define BNO055_IMU_H

#include <Adafruit_BNO055.h>

class MyBNO055 {
public:
    MyBNO055();
    bool begin();
    void getOrientation(float* roll, float* pitch, float* yaw);

private:
    Adafruit_BNO055 bno;
};

#endif


