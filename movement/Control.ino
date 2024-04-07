#include <Ethernet.h>
#include <EthernetUdp.h>
#include "ESC.h"
#include "PressureSensor.h"
#include "BNO055_IMU.h"

#define NUMBER_OF_THRUSTERS 6
#define CHECKSUM_SIZE 1
#define SEND_BUFFER_SIZE 1 
#define BUFFER_SIZE (CHECKSUM_SIZE + NUMBER_OF_THRUSTERS)
#define PRESSURE_READINGS 1
#define IMU_READINGS 3
#define SEND_BUFFER_SIZE (CHECKSUM_SIZE + PRESSURE_READINGS + IMU_READINGS)

byte mac[] = {0x2C, 0xF7, 0xF1, 0x08, 0x30, 0x84};
unsigned int localPort = 8888;
byte receiveBuffer[BUFFER_SIZE];
byte sendBuffer[SEND_BUFFER_SIZE];
EthernetUDP Udp;
EscControl thrusters[NUMBER_OF_THRUSTERS] = {EscControl(9), EscControl(10), EscControl(11), EscControl(12), EscControl(13), EscControl(14)};
PressureSensor pressureSensor;
MyBNO055 myIMU;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < NUMBER_OF_THRUSTERS; i++) {
    thrusters[i].init();
  }
  setupUDP();
  pressureSensor.begin();
  myIMU.begin();
}

void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    int len = Udp.read(receiveBuffer, BUFFER_SIZE);
    
    if (len == BUFFER_SIZE) {
      readData(receiveBuffer);
    } else {
      Serial.println("Invalid packet format or size, discarding packet.");
    }
  }

  //send pressure reading back
  float pressureReading = pressureSensor.readPressure();
  byte pressureByte = static_cast<byte>(pressureReading);

  //assemble send buffer
  sendBuffer[1] = pressureByte;
  //get orientation data from IMU
  float roll, pitch, yaw;
  readIMUData(roll,pitch,yaw);

  // Send pressure packet
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(sendBuffer, SEND_BUFFER_SIZE);
  Udp.endPacket();

  delay(1000); // Adjust delay as necessary
}

void setupUDP() {
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  Udp.begin(localPort);
}

void readData(byte packetBuffer[]) {
  // Extracting checksum from the packet
  int received_checksum = 0;
  memcpy(&received_checksum, packetBuffer, CHECKSUM_SIZE);

  // Extracting thruster values from the packet
  byte thrusterValues[NUMBER_OF_THRUSTERS];
  memcpy(thrusterValues, packetBuffer + CHECKSUM_SIZE, NUMBER_OF_THRUSTERS);

  // Verifying the checksum
  if (checksum(thrusterValues, received_checksum)) {
    for (int j = 0; j < NUMBER_OF_THRUSTERS; j++) {
      // Update the thruster ESCs
      thrusters[j].updateEsc(thrusterValues[j]);
    }
  } else {
    Serial.println("Checksum validation failed. Packet has not been registered.");
  }
}

// Checksum method, uses XOR and compares calculated and received values
bool checksum(byte thrusterValues[], int received_checksum) {
  int calculated_checksum = thrusterValues[0];
  for (int i = 1; i < NUMBER_OF_THRUSTERS; i++) {
    // XOR
    calculated_checksum ^= thrusterValues[i];
  }
  // Compare with the checksum received in the packet
  return calculated_checksum == received_checksum;
}

byte mapValueToByte(float value) {
  // Map the value range of 0 to 360 to the byte range of 0 to 255
  float mappedValue = (value / 360.0) * 255.0;
  // Round the mapped value to the nearest integer
  mappedValue = round(mappedValue);
  // Ensure the mapped value stays within the range of 0 to 255
  return static_cast<byte>(constrain(mappedValue, 0, 255));
}

void readIMUData(float roll,float pitch,float yaw) {
  myIMU.getOrientation(&roll, &pitch, &yaw);
  // Scale orientation data to fit within the range of 0 to 255
  byte rollByte = mapValueToByte(roll);
  byte pitchByte = mapValueToByte(pitch);
  byte yawByte = mapValueToByte(yaw);
  // Assemble send buffer for orientation data
  sendBuffer[2] = rollByte;
  sendBuffer[3] = pitchByte;
  sendBuffer[4] = yawByte;
}




