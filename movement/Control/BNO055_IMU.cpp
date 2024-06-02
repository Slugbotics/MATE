#include "BNO055_IMU.h"

MyBNO055::MyBNO055() : bno(55, 0x28, &Wire) {}

bool MyBNO055::begin() {
    return bno.begin();
}

void MyBNO055::getOrientation(float* roll, float* pitch, float* yaw) {
    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
    *roll = orientationData.orientation.x;
    *pitch = orientationData.orientation.y;
    *yaw = orientationData.orientation.z;
}

void MyBNO055::getAcceleration(float* x, float* y, float* z){
    sensors_event_t accelerationData;
    bno.getEvent(&accellerationData, Adafruit_BNO055::VECTOR_ACCELEROMETER);
    *x = accelerationData.acceleration.x;
    *y = accelerationData.acceleration.y;
    *z = accelerationData.acceleration.z;
}
