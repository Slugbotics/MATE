#include <Ethernet.h>
#include <EthernetUdp.h>
#include "ESC.h"
#include "BNO055_IMU.h"
#include "Arm.h"

#define RESET_PIN 8
#define NUMBER_OF_THRUSTERS 6
#define NUMBER_OF_SERVOS 4
#define CHECKSUM_SIZE 1
#define SEND_BUFFER_SIZE 1 
#define BUFFER_SIZE (CHECKSUM_SIZE + NUMBER_OF_THRUSTERS + NUMBER_OF_SERVOS)
#define IMU_READINGS 3
#define SEND_BUFFER_SIZE (CHECKSUM_SIZE + IMU_READINGS)

byte mac[] = {0xA8, 0x61, 0x0A, 0xAE, 0x95, 0xE3 };
IPAddress ip(192, 168, 1, 177);
unsigned int localPort = 8888;
byte receiveBuffer[BUFFER_SIZE];
byte sendBuffer[SEND_BUFFER_SIZE];
EthernetUDP Udp;
EscControl thrusters[NUMBER_OF_THRUSTERS] = {EscControl(9), EscControl(10), EscControl(11), EscControl(12), EscControl(13), EscControl(14)};
ServoControl servos[NUMBER_OF_SERVOS] = {ServoControl(15), ServoControl(16), ServoControl(17), ServoControl(19)};
MyBNO055 myIMU;
double PACKET_SCALAR = 1.41732;

void setup() {
  Serial.begin(9600);
  pinMode(RESET_PIN, OUTPUT);
  digitalWrite(RESET_PIN, HIGH);
  for (int i = 0; i < NUMBER_OF_THRUSTERS; i++) {
    thrusters[i].init();
  }
  for (int j = 0; j < NUMBER_OF_SERVOS; j++) {
    servos[j].init();
  }
  setupUDP();
  myIMU.begin();
}

 void rst(){
  digitalWrite(RESET_PIN, LOW);
  delay(1000);
  digitalWrite(RESET_PIN, HIGH);
}

void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    int len = Udp.read(receiveBuffer, BUFFER_SIZE);
    Serial.println(len);
    
    if (len == BUFFER_SIZE) {
      readData(receiveBuffer);
    } else {
      Serial.println("Restarting...");
      rst();
    }
  }

  //get acceleration data from IMU
  float x, y, z;
  readIMUData(x,y,z);

  //send outgoing packet
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(sendBuffer, SEND_BUFFER_SIZE);
  Udp.endPacket();

}

void setupUDP() {
 // if (!Ethernet.begin(mac, ip)) {
   // Serial.println("Failed to configure Ethernet using DHCP");
  //}
  Ethernet.begin(mac,ip);
  Udp.begin(localPort);
  delay(100);
  Serial.println("---ETHERNET CONNECTION ESTABLISHED---");
}

void readData(byte packetBuffer[]) {
  //extracting checksum from the packet
  int received_checksum = 0;
  memcpy(&received_checksum, packetBuffer, CHECKSUM_SIZE);

  //xtracting thruster values from the packet
  byte thrusterValues[NUMBER_OF_THRUSTERS];
  memcpy(thrusterValues, packetBuffer + CHECKSUM_SIZE, NUMBER_OF_THRUSTERS);
  
  //extracting servo displacement values from the packet
  byte servoDisplacement[NUMBER_OF_SERVOS];
  memcpy(servoDisplacement, packetBuffer + CHECKSUM_SIZE + NUMBER_OF_THRUSTERS, NUMBER_OF_SERVOS);

  //verifying the checksum
  //if (checksum(thrusterValues, received_checksum)) {
    for (int j = 0; j < NUMBER_OF_THRUSTERS; j++) {
      //update the thruster ESCs
      thrusters[j].updateEsc(thrusterValues[j]);
      // Serial.print("Thruster: ");
      // Serial.println(thrusterValues[j]);
    }
    for (int k = 0; k < NUMBER_OF_SERVOS; k++) {
      //update the servo positions
      servos[k].write(servoDisplacement[k]);
      // Serial.print("Arm: ");
      // Serial.println(servoDisplacement[k]);
    }
  //} else {
  //  Serial.println("Checksum validation failed. Packet has not been registered.");
 // }
}

//checksum method, uses XOR and compares calculated and received values
bool checksum(byte thrusterValues[], int received_checksum) {
  int calculated_checksum = thrusterValues[0];
  for (int i = 1; i < NUMBER_OF_THRUSTERS; i++) {
    //xor
    calculated_checksum ^= thrusterValues[i];
  }
  //compare with the checksum received in the packet
  return calculated_checksum == received_checksum;
}

byte mapValueToByte(float value) {
  //map the value range of 0 to 360 to the byte range of 0 to 255
  float mappedValue = (value / 360.0) * 255.0;
  //round the mapped value to the nearest integer
  mappedValue = round(mappedValue);
  //cast to make sure mapped value stays within the range of 0 to 255
  return static_cast<byte>(constrain(mappedValue, 0, 255));
}

void readIMUData(float x,float y,float z) {
  myIMU.getOrientation(&x, &y, &z);
  //scale orientation data to fit within the range of 0 to 255
  byte xByte = mapValueToByte(x);
  byte yByte = mapValueToByte(y);
  byte zByte = mapValueToByte(z);
  //assemble send buffer for orientation data
  sendBuffer[1] = rollByte;
  sendBuffer[2] = pitchByte;
  sendBuffer[3] = yawByte;
}