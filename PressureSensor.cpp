#include "PressureSensor.h"

PressureSensor::PressureSensor(int8_t reset_pin, int8_t EOC_pin) : mpr(reset_pin, EOC_pin) {}

bool PressureSensor::begin() {
    return mpr.begin();
}

float PressureSensor::readPressure() {
    return mpr.readPressure();
}

float PressureSensor::calculateDepth(float pressure) {
    if (pressure <= 0) {
        return 0.0;
    } else {
        const float FLUID_DENSITY = 1000.0;
        const float GRAVITY = 9.81;
        float depth = (pressure * 100) / (FLUID_DENSITY * GRAVITY);
        return depth;
    }
}

