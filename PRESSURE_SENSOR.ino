#include <Wire.h>
#include "PressureSensor.h"

#define RESET_PIN  -1
#define EOC_PIN    -1
PressureSensor pressureSensor(RESET_PIN, EOC_PIN);

void setup() {
  Serial.begin(115200);
  Serial.println("MPRLS:");
  if (! pressureSensor.begin()) {
    Serial.println("Failed to communicate with MPRLS sensor, check wiring?");
    while (1) {
      delay(10);
    }
  }
  Serial.println("Found MPRLS sensor");
}

void loop() {
  float pressure_hPa = pressureSensor.readPressure();
  Serial.print("Pressure (hPa): "); Serial.println(pressure_hPa);
  Serial.print("Pressure (PSI): "); Serial.println(pressure_hPa / 68.947572932);
  Serial.print("Depth (m): "); Serial.println(pressureSensor.calculateDepth(pressure_hPa));
  delay(1000);
}


