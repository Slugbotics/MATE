#include <Ethernet.h>
#include <EthernetUdp.h>
#include "ESC.h"//esc control file

EscControl thrusterControl(9); // Specify the ESC pin

#define MAX_STRING_LENGTH 4
#define NUMBER_OF_STRINGS 6
#define DELIMITER_SIZE 1
#define BUFFER_SIZE (MAX_STRING_LENGTH * NUMBER_OF_STRINGS + (NUMBER_OF_STRINGS - 1) * DELIMITER_SIZE)

byte mac[]={0};//idk mac address
unsigned int localPort = 8888;//using a random registered port
char packetBuffer[BUFFER_SIZE];//array to hold data
EthernetUDP Udp;//udp object

void setup() {
  Serial.begin(9600);//9600 baud rate
  
  thrusterControl.init();//initialize ESC control

  //check if the ethernet connection fails or not
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
  }
  Udp.begin(localPort);//initialize udp instance
}

void loop() {
  int packetSize = Udp.parsePacket();//get size of packet
  if (packetSize) {//if its no zero
    Udp.read(packetBuffer, BUFFER_SIZE);//read packet to length of buffer to prevent indexing error
    int joystickValue = atoi(packetBuffer);//converts string to int, we could also use strtol for error handling but its probably fine
    
    thrusterControl.updateEsc(joystickValue);//update esc function

    //some debugging code
    Serial.print("Joystick: ");
    Serial.print(joystickValue);
    Serial.print(", ESC: ");
    Serial.println(thrusterControl.getEscValue());
  }
}

