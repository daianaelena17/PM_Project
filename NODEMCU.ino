#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#include <SPI.h>
#ifndef HAVE_HWSERIAL3
#endif 
const char* ssid = "Hogwarts Great Hall Wifi";
const char* password = "************";
const char* host = "192.168.0.22";
int s135 = 0;
int s7 = 0;
int MZ = 0;
int s5 = 0;
int ledPin = D8;
WiFiServer server(3601);

void setup() {
  Serial.begin(9600);
  Serial.println(WiFi.localIP());
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  server.begin();
  Serial.println("Server started");
  Serial.println(WiFi.localIP());
}


void loop() {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  while (!client.available()) {
    delay(1);
  }
  String req = client.readStringUntil('\r');
  client.flush();
  int ok = 0;
  // Match the request
  digitalWrite(ledPin, LOW);
  
  if (req.indexOf("") != -1) {  //checks if you're on the main page

    if (req.indexOf("/ON") != -1) { //checks if you clicked ON
      if (Serial.available() > 0) {
      StaticJsonBuffer<5000> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(Serial);
      if (root == JsonObject::invalid()){
        JsonObject& root = jsonBuffer.parseObject(Serial);
        return;
      }
      ok = 1;
      s135 = root["val 135"];
      s7 = root["val 7"];
      s5 = root["val 5"];
      MZ = root["MHZ14A"];
      Serial.println("JSON received and parsed");
      root.prettyPrintTo(Serial);
      digitalWrite(ledPin, HIGH);
      Serial.println("\n");
      Serial.println("You got new data");
      }
    }
  }

  else {
    Serial.println("invalid request");
   client.stop();
    return;
  } 
  // Prepare the response
  
  String s = "HTTP/1.1 200 OK\r\n";
  s += "Content-Type: text/html\r\n\r\n";
  s += "<!DOCTYPE HTML>\r\n<html>\r\n";
  s += "Location = Agigea";
  s += "<br><br><br>";
  if (ok == 1) {
    s += "<b>Data from MQ135 = </b>";
    s += s135;
    s += "<br>";
    s += "<b>Data from MQ7 = </b>";
    s += s7;
    s += "<br>";
    s += "<b>Data from MQ5 = </b>";
    s += s5;
    s += "<br>";
    s += "<b>Data from MHZ14A = </b>";
    s += MZ;
    s += "<br>";
  }
  s += "<br><input type=\"button\" name=\"bl\" value=\"GET NEW DATA FROM SENSORS\" onclick=\"location.href='/ON'\">";
  s += "<br><br><br>";
  s += "</html>\n";

  client.flush();

  // Send the response to the client
  client.print(s);
}
