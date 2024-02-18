#include "PressureSensor.h"

const float FLUID_DENSITY = 1000.0;
const float GRAVITY = 9.81;

PressureSensor::PressureSensor(int8_t reset_pin, int8_t EOC_pin,
                               uint16_t PSI_min, uint16_t PSI_max,
                               float OUTPUT_min, float OUTPUT_max,
                               float K) : mprls(reset_pin, EOC_pin, PSI_min, PSI_max, OUTPUT_min, OUTPUT_max, K) {}

bool PressureSensor::begin(uint8_t i2c_addr, TwoWire *twoWire) {
    return mprls.begin(i2c_addr, twoWire);
}

uint8_t PressureSensor::readStatus() {
    return mprls.readStatus();
}

float PressureSensor::readPressure() {
    return mprls.readPressure();
}
float PressureSensor::calculateDepth(float pressure){
    float depth = pressure / (FLUID_DENSITY * GRAVITY);
    return depth;
}