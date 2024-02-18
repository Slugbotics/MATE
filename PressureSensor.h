#ifndef PRESSURESENSOR_H
#define PRESSURESENSOR_H

#include <stdint.h> 
#include <Wire.h> 
#include <Adafruit_MPRLS.h> 

#define MPRLS_DEFAULT_ADDR 0x28
#define PSI_to_HPA 0.625

class PressureSensor {
public:
    PressureSensor(int8_t reset_pin = -1, int8_t EOC_pin = -1,
                   uint16_t PSI_min = 0, uint16_t PSI_max = 25,
                   float OUTPUT_min = 10, float OUTPUT_max = 90,
                   float K = PSI_to_HPA);

    bool begin(uint8_t i2c_addr = MPRLS_DEFAULT_ADDR, TwoWire *twoWire = &Wire);
    uint8_t readStatus();
    float readPressure();
    float calculateDepth(float pressure);

private:
    Adafruit_MPRLS mprls;
};

#endif
