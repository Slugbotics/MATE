#include <Wire.h>
#include <stdint.h>
#include "PressureSensor.h"

const int8_t RESET_PIN = 7;
const int8_t EOC_PIN = 11;

const uint16_t PSI_MIN = 0;
const uint16_t PSI_MAX = 100;

const float OUTPUT_MIN = 0.5;
const float OUTPUT_MAX = 4.5;

const float K = 0.625;

const uint8_t I2C_ADDR = 0x28;

PressureSensor pressureSensor(RESET_PIN, EOC_PIN, PSI_MIN, PSI_MAX, OUTPUT_MIN, OUTPUT_MAX, K);

void setup() {
  Serial.begin(9600);
  //initialize I2C communication
  Wire.begin();
  if (!pressureSensor.begin(I2C_ADDR, &Wire)) {
    Serial.println("Error initializing PressureSensor!");
    while (1);
  }
}

void loop() {
  //read pressure from the sensor
  float pressure = pressureSensor.readPressure();
  //print pressure to serial monitor
  Serial.print("Pressure (PSI): ");
  Serial.println(pressure);
  
  //calculate depth using the pressure
  float depth = pressureSensor.calculateDepth(pressure);
  Serial.print("Depth (m): ");
  Serial.println(depth);
  //delay
  delay(1000);
}

