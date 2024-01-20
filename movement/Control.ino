#include <Ethernet.h>
#include <EthernetUdp.h>
//esc control file
#include "ESC.h"

//PUBLIC
#define MAX_STRING_LENGTH 4
#define NUMBER_OF_STRINGS 6
#define DELIMITER_SIZE 1
#define BUFFER_SIZE (MAX_STRING_LENGTH * NUMBER_OF_STRINGS + (NUMBER_OF_STRINGS - 1) * DELIMITER_SIZE)
//mac address, look on the back the arduino
byte mac[]={0x2C,0xF7,0xF1,0x08,0x30,0x84};
//using a random registered port
unsigned int localPort = 8888;
//array to hold data
char packetBuffer[BUFFER_SIZE];
//udp object
EthernetUDP Udp;
//esc pin reference for 6 thrusters
EscControl thrusters[NUMBER_OF_THRUSTERS] = {EscControl(9), EscControl(10), EscControl(11), EscControl(12), EscControl(13), EscControl(14)};

void setup() {
  //9600 baud rate
  Serial.begin(9600);
  //initialize ESC control
  for (int i = 0; i < NUMBER_OF_THRUSTERS; i++) {
    thrusters[i].init();
  }
  //connection setup
  void setupUDP()
}

void loop() {
  //get size of packet
  int packetSize = Udp.parsePacket();
  //call read data function
  if (packetSize) {
    //read packet into the buffer
    Udp.read(packetBuffer, BUFFER_SIZE);
    //set null terminator
    packetBuffer[packetSize] = '\0';
    readData(packetSize)
  }
}

void setupUDP(){
  //check if the ethernet connection fails or not
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  //initialize udp instance
  Udp.begin(localPort);
}

void readData(char packetBuffer[]) {
  //split to segment at delimiter
  char* token = strtok(packetBuffer, ",");
  //pointer to end of segment
  char* endPtr;
  int i = 0;
  while (token != NULL && i < NUMBER_OF_THRUSTERS) {
    //convert string to int with strtol(segment pointer, pointer to start, base)
    long joystickValue = strtol(token, &endPtr, 10);
    //if the end pointer is not pointing to token and within range
    if (token != endPtr && joystickValue>=0 && joystickValue<=200) {
      thrusters[i].updateEsc(joystickValue);
      i++;
    } else {
      Serial.print("Invalid input: ");
      Serial.print(joystickValue);

    }
    //get the next token
    token = strtok(NULL, ",");
  }
  /*
  //debugging code
  Serial.print("Thruster values: ");
  for (int j = 0; j < NUMBER_OF_THRUSTERS; j++) {
    Serial.print(thrusters[j].getEscValue());
    if (j < NUMBER_OF_THRUSTERS - 1) {
      Serial.print(", ");
    }
  }
  */
}

void checksum(){
  return
}

