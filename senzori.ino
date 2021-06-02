#include <SoftwareSerial.h>
#include <ArduinoJson.h>

int pinMQ135 = A0;
int pinMQ7 = A5;
int pinMQ5 = A4;
int pinBuzz = 7;

int val135 = 0;
int val7 = 0;
int val5 = 0;
int MHZ14A = 0;

SoftwareSerial sensor(10, 11); // RX, TX
const byte requestReading[] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79};
byte result[9];


void setup() {
  Serial.begin(9600);
  sensor.begin(9600);
  digitalWrite(pinBuzz, LOW);
  pinMode(pinMQ135, INPUT);
  pinMode(pinMQ7, INPUT);
  pinMode(pinMQ5, INPUT);
}

int readPPMSerial() {
  for (int i = 0; i < 9; i++) {
    sensor.write(requestReading[i]); 
  }
  //Serial.println("sent request");
  while (sensor.available() < 9) {}; // wait for response
  for (int i = 0; i < 9; i++) {
    result[i] = sensor.read(); 
  }
  int high = result[2];
  int low = result[3];
    //Serial.print(high); Serial.print(" ");Serial.println(low);
  return high * 256 + low;
}


void loop() {
//  Serial.println("dc eu?\n");
  StaticJsonBuffer<5000> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();

  val135 = analogRead(pinMQ135);
  val7 = analogRead(pinMQ7);
  val5 = analogRead(pinMQ5);
  MHZ14A = readPPMSerial();
 
  root["val 135"] = val135;
  root["val 7"] = val7;
  root["val 5"] = val5;
  root["MHZ14A"] = MHZ14A;

  if (val135 > 1000 || val7 > 1800 || val5 > 500 || MHZ14A > 2000) {
    digitalWrite(pinBuzz, HIGH);
  }
  
  if (Serial.available() > 0) {
    root.printTo(Serial);
  }
  delay(3000);
  digitalWrite(pinBuzz, LOW);

}
