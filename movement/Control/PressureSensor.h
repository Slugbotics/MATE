#ifndef PRESSURESENSOR_H
#define PRESSURESENSOR_H

#include <Wire.h>
#include "Adafruit_MPRLS.h"

class PressureSensor {
public:
    PressureSensor(int8_t reset_pin = -1, int8_t EOC_pin = -1);
    bool begin();
    float readPressure();

private:
    Adafruit_MPRLS mpr;
};

#endif
