#include <Ethernet.h>
#include <EthernetUdp.h>
//esc control file
#include "ESC.h"
//esc pin reference
EscControl thrusterControl(9);

#define MAX_STRING_LENGTH 4
#define NUMBER_OF_STRINGS 6
#define DELIMITER_SIZE 1
#define BUFFER_SIZE (MAX_STRING_LENGTH * NUMBER_OF_STRINGS + (NUMBER_OF_STRINGS - 1) * DELIMITER_SIZE)
//idk mac address
byte mac[]={0};
//using a random registered port
unsigned int localPort = 8888;
//array to hold data
char packetBuffer[BUFFER_SIZE];
//udp object
EthernetUDP Udp;
//9600 baud rate
void setup() {
  Serial.begin(9600);
  //initialize ESC control
  thrusterControl.init();

  //check if the ethernet connection fails or not
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  //initialize udp instance
  Udp.begin(localPort);
}

void loop() {
  //get size of packet
  int packetSize = Udp.parsePacket();
  //if its no zero
  if (packetSize) {
    //read packet to length of buffer to prevent indexing error
    Udp.read(packetBuffer, BUFFER_SIZE);
    //converts string to int, we could also use strtol for error handling but its probably fine
    int joystickValue = atoi(packetBuffer);
    //update esc function
    thrusterControl.updateEsc(joystickValue);

    //some debugging code
    Serial.print("Joystick: ");
    Serial.print(joystickValue);
    Serial.print(", ESC: ");
    Serial.println(thrusterControl.getEscValue());
  }
}

