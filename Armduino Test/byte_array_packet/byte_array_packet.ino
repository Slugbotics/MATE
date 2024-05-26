#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Servo.h>
#include <stdio.h>
#define ELEMENT_SIZE 1
#define BUFFER_SIZE 11
#define ARM_STARTING_POINT 7
#define ARM_ENDING_POINT 9
#define X 1<<7 
#define B 1<<6 
#define START 1<<5 
#define LEFT_BUMPER 1<<4 
#define RIGHT_BUMPER 1<<3 

// Ethernet settings
byte mac[] = {
  0xA8, 0x61, 0x0A, 0xAE, 0x95, 0xE3 };
IPAddress ip(192, 168, 1, 177); //Server IP
unsigned int localPort = 8888;
byte receiveBuffer[BUFFER_SIZE+1];
byte sendBuffer[BUFFER_SIZE];

// Initialize the Ethernet and UDP
EthernetUDP Udp;

// Arm Servos
Servo horizontalServo;
Servo verticalServo;

Servo wristServo;
Servo clawServo;

int8_t horizontal = 0;
int start_horizontal = 90;
int horizontal_scalar = 3;

int8_t vertical = 0;
int start_vertical = 90;
int vertical_scalar = 3;

int wristRotValue = 90;
int wristRot_scalar = 1;

int clawRotValue = 90;
int clawRot_scalar = 1;

int claw_increase = 0; // left bumper
int claw_decrease = 0; // right bumper

int wrist_increase = 0; // x
int wrist_decrease = 0; // b

int start = 0;

int arm_bools = 0;

int packetSize = 0;
void setup() {
  // Start Ethernet and UDP
  Ethernet.begin(mac, ip);
  Udp.begin(localPort);

  // Attach servos to pins
  horizontalServo.attach(8);
  verticalServo.attach(9);

  wristServo.attach(10);
  clawServo.attach(11);

  Serial.begin(9600);

  // Setup other outputs
}

// int count = 0;
void loop() {
  packetSize = Udp.parsePacket();
  if (packetSize && packetSize <= BUFFER_SIZE) {
    // Receive packet
    Udp.read(receiveBuffer, packetSize);
    // count++;
    // Serial.println(count);
    receiveBuffer[packetSize] = '\0';
    for (int i =0; i < packetSize; i++){
      Serial.print(receiveBuffer[i]); 
    }
    Serial.print("\n");

    horizontal = receiveBuffer[ARM_STARTING_POINT] - 10;
    vertical = receiveBuffer[ARM_STARTING_POINT + ELEMENT_SIZE] - 10;
    arm_bools = receiveBuffer[ARM_ENDING_POINT];

    // extract booleans from servo2
    claw_increase = (arm_bools == LEFT_BUMPER) ? 1 : 0;
    claw_decrease = (arm_bools == RIGHT_BUMPER) ? 1 : 0;
    wrist_increase = (arm_bools == X) ? 1 : 0;
    wrist_decrease = (arm_bools == B) ? 1: 0;
    start = (arm_bools == START) ? 1: 0;

    Serial.print("bools: ");
    Serial.print(arm_bools);
    Serial.print("\n");

    // char temp[5];

    horizontal *= horizontal_scalar;
    vertical *= vertical_scalar;
    
    // Control servos
    if((start_horizontal + horizontal) < 180 && (start_horizontal + horizontal) > 0){
     horizontalServo.write(start_horizontal += horizontal);
    }
    if (horizontal < -10){
      horizontal = 0;
    }

    if((start_vertical + vertical) < 180 && (start_vertical + vertical) > 0){
      verticalServo.write(start_vertical += vertical);
    }

    wristServo.write(wrist(wrist_increase, wrist_decrease, 15));

    clawServo.write(claw(claw_increase, claw_decrease, 15));
   }
   if (packetSize > BUFFER_SIZE) {
    Serial.print("DIED\n");
    goto loop;
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