//website Transmiter and Receiver:https://lastminuteengineers.com/nrf24l01-arduino-wireless-communication/
//Include Libraries
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <RTClib.h>
#include <Wire.h>
#include <Servo.h>

//----- Pin Definitions ----
int pressureSensor = A2;
int motorPins[6] = {2,3,4,5,6,7};
int CERadioPin = 9;
int CSNRadioPin = 8;

//---- Changeable Parameters
int SerialBaudRate = 9600;
int speedcontrol = 45;
const int NumofMotors = 6;
const char* CompnayNumber = " Company Number: Slugbotics";

//address through which two modules communicate.
const byte address[6] = "00001";

//---- Object Definitons ----
Servo motors[NumofMotors];
RTC_DS3231 rtc;
RF24 radio(CERadioPin, CSNRadioPin);  // CE, CSN


char t[32];
char text[100];

void updateRTC(){
  const char txt[6][15] = { "year [4-digit]", "month [1~12]", "day [1~31]",
                            "hours [0~23]", "minutes [0~59]", "seconds [0~59]"};
  String str = "";
  long newDate[6];
  // Grabs all user inputs
  for (int i = 0; i < 6; i++){
    Serial.print("Enter ");
    Serial.print(txt[i]);
    Serial.print(":");
    str = Serial.readString();
    newDate[i] = str.toInt();
    Serial.println(newDate[i]); 
  }
  // Update the RTC
  rtc.adjust(DateTime(newDate[0], newDate[1], newDate[2], newDate[3], newDate[4], newDate[5]));
  Serial.println("RTC Updated");
}

void setup()
{
    while (!Serial);
    Serial.begin(SerialBaudRate);
    // Attach all of the motors
    for (int i = 0; i < NumofMotors; i++){
      motors[i].attach(motorPins[i]);
    }
    // Start RTC Module
    rtc.begin();
  // Start Radio Module
  radio.begin();
  
  //set the address
  radio.openWritingPipe(address);
  
  //Set module as transmitter
  radio.stopListening();
}
void loop()
{
  if (Serial.available()) {
    char input = Serial.read();
    if (input == 'u') updateRTC();  // update RTC time
  }
  // Need to work on pressure sensor activation when it bottom of the pool or not
  int value = analogRead(pressureSensor);
  Serial.print("Pressure reading: ");
  Serial.println(value);
  delay(200);
  
  boolean ReachedSurface = false;
  // Controls Motor to 360 forward and 360 backward
  for (int i = 0; i < NumofMotors; i++){
    for (int pos = 0; pos <= 360; pos++){
      motors[i].write(pos);
    }
  }
  
  for (int i = 0; i < NumofMotors; i++){
    for (int pos = 360; pos >= 0; pos--){
      motors[i].write(pos);
    }
  }
  
  //current time
  if (ReachedSurface){
    DateTime now = rtc.now();
    sprintf(t, "%02d:%02d:%02d %02d/%02d/%02d", now.hour(), now.minute(), now.second(), now.day(), now.month(), now.year());
    //Send message to receiver
    strcpy(text, t);
    strcat(text, CompnayNumber);
    //const char text[] = "Hello World " + t + CompanyNumber;
    radio.write(&text, sizeof(text));
    Serial.println("Sending,text: ");
    Serial.println(text);
    delay(1000);
  }
}
