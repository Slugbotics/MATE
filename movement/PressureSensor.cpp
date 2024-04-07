#include "PressureSensor.h"

PressureSensor::PressureSensor(int8_t reset_pin, int8_t EOC_pin) : mpr(reset_pin, EOC_pin) {}

bool PressureSensor::begin() {
    return mpr.begin();
}

float PressureSensor::readPressure() {
    return mpr.readPressure();
}
