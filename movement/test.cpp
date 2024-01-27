#include <ArduinoUnit.h>
#include "ESC.h"

#define NUMBER_OF_THRUSTERS 6

//pin references
int EscPins[NUMBER_OF_THRUSTERS] = {9, 10, 11, 12, 13, 14};
//correct thruster values
int ValidEscValues[NUMBER_OF_THRUSTERS] = {50, 60, 70, 80, 90, 100};
//test packet with valid values
char testPacket[] = "50,60,70,80,90,100";
//test packet with invalid values
char testPacket2[] = "-1,60,70,80,90,300";

//test if thrusters are initialized to 0
test(ESCControlInitialization) {
  //initialize object
  EscControl thrusters[NUMBER_OF_THRUSTERS];
  for (int i = 0; i < NUMBER_OF_THRUSTERS; i++) {
    //pin references
    thrusters[i] = EscControl(EscPins[i]);
    //check if thrusters initialize function works correctly and starts them at rest
    assertEqual(thrusters[i].getEscValue(), 0);
  }
  //shut off thrusters
}

test(ValidEscUpdate) {
  //initialize ESC controls and set to 0
  EscControl thrusters[NUMBER_OF_THRUSTERS];
  for (int i = 0; i < NUMBER_OF_THRUSTERS; i++) {
    thrusters[i] = EscControl(EscPins[i]);
  }

  //call readData with the simulated packet size
  readData(testPacket);

  //verify that the invalid values were not set
  assertEqual(thrusters[0].getEscValue(), 50);
  assertEqual(thrusters[1].getEscValue(), 60);
  assertEqual(thrusters[2].getEscValue(), 70);
  assertEqual(thrusters[3].getEscValue(), 80);
  assertEqual(thrusters[4].getEscValue(), 90);
  assertEqual(thrusters[5].getEscValue(), 100);

  //verify valid values were updated correctly
  for (int i = 1; i < NUMBER_OF_THRUSTERS - 1; i++) {
    int expectedValue = atoi(strtok(i == 1 ? testPacket : NULL, ","));
    assertEqual(thrusters[i].getEscValue(), expectedValue);
  }
}

test(InvalidEscUpdate) {
  //initialize ESC controls and set to 0
  EscControl thrusters[NUMBER_OF_THRUSTERS];
  for (int i = 0; i < NUMBER_OF_THRUSTERS; i++) {
    thrusters[i] = EscControl(EscPins[i]);
  }

  //call readData with the simulated packet size
  readData(testPacket2);

  //verify that the invalid values were not set
  assertEqual(thrusters[0].getEscValue(), 0);
  assertEqual(thrusters[1].getEscValue(), 0);
  assertEqual(thrusters[2].getEscValue(), 0);
  assertEqual(thrusters[3].getEscValue(), 0);
  assertEqual(thrusters[4].getEscValue(), 0);
  assertEqual(thrusters[5].getEscValue(), 0);

  //verify valid values were updated correctly
  for (int i = 1; i < NUMBER_OF_THRUSTERS - 1; i++) {
    int expectedValue = atoi(strtok(i == 1 ? testPacket2 : NULL, ","));
    assertEqual(thrusters[i].getEscValue(), expectedValue);
  }
}


//test checksum
test(ValidCheckSum) {

}

void setup() {
  //mac address, look on the back the arduino
  byte mac[]={0x2C,0xF7,0xF1,0x08,0x30,0x84};
  //using a random registered port
  unsigned int localPort = 8888;
  //array to hold data
  char packetBuffer[BUFFER_SIZE];
  //udp object
  EthernetUDP Udp;
  Test::run();
}


