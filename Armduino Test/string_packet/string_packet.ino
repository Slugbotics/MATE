#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Servo.h>

// Ethernet settings
byte mac[] = {  
  0xA8, 0x61, 0x0A, 0xAE, 0x95, 0xE3 };
IPAddress ip(192, 168, 1, 177); //Server IP
unsigned int localPort = 8888;

// Initialize the Ethernet and UDP
EthernetUDP Udp;

// Arm Servos
Servo horizontalServo;
Servo verticalServo;

Servo wristServo;
Servo clawServo;

int start_horizontal = 90;
int horizontal_scalar = 1;

int start_vertical = 90;
int vertical_scalar = 1;

int wristRotValue = 90;
int wristRot_scalar = 1;

int clawRotValue = 90;
int clawRot_scalar = 1;

void setup() {
  // Start Ethernet and UDP
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);

  // Attach servos to pins
 // horizontalServo.attach(8);
  //verticalServo.attach(9);

  verticalServo.attach(9);

  //wristServo.attach(2);
  //clawServo.attach(3);

  Serial.begin(9600);

  // Setup other outputs
}

void loop() {
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    // Receive packet
    char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    Serial.println(packetBuffer);



    // Parse packet
    int horizontal, vertical, claw_decrease, claw_increase, wrist_decrease, wrist_increase;
    sscanf(packetBuffer, "%d %d %d %d %d %d %*d",
     &horizontal, &vertical, &wrist_increase, &wrist_decrease, &claw_increase, &claw_decrease);

    horizontal *= - horizontal_scalar;
    vertical *= - vertical_scalar;
    
    // Control servos
    if((start_horizontal + horizontal) < 180 && (start_horizontal + horizontal) > 0){
     horizontalServo.write(start_horizontal += horizontal);
     Serial.println(start_horizontal += horizontal);
    }

    if((start_vertical + vertical) < 180 && (start_vertical + vertical) > 0){
      verticalServo.write(start_vertical += vertical);
    }

    wristServo.write(wrist(wrist_increase, wrist_decrease, 15));

    clawServo.write(claw(claw_increase, claw_decrease, 15));
   }
}

int wrist(int increase, int decrease, int delta) {
  int idk = wristRotValue;
  if (increase && !decrease && wristRotValue < (180-delta)){
    wristRotValue += delta;
    idk = wristRotValue;
  }
  if (decrease && !increase && wristRotValue > (0+delta)){
    wristRotValue -= delta;
    idk = wristRotValue;
  }
  return idk;
}

int claw(int increase, int decrease, int delta){
  int idk = clawRotValue;
  if (increase && !decrease && clawRotValue < (180-delta)){
    clawRotValue += delta;
    idk = clawRotValue;
  }
  if (decrease && !increase && clawRotValue > (0+delta)){
    clawRotValue -= delta;
    idk = clawRotValue;
  }
  return idk;
}