#include <Wire.h>
#include "BNO055_IMU.h"

MyBNO055 bnoSensor;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);  // wait for serial port to open!

  Serial.println("Orientation Sensor Test");

  if (!bnoSensor.begin()) {
    Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  delay(1000);
}

void loop() {
  float roll, pitch, yaw;
  bnoSensor.getOrientation(&roll, &pitch, &yaw);

  Serial.print("Roll: ");
  Serial.print(roll);
  Serial.print(" | Pitch: ");
  Serial.print(pitch);
  Serial.print(" | Yaw: ");
  Serial.println(yaw);

  delay(100);
}

