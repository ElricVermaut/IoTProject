#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>
//#include <HTTPClient.h>
//#include <HttpClient.h>
#include <WiFiNINA.h>
#include "arduino_secrets.h"
#include "DHT.h"
#include <LiquidCrystal.h>
#include <SPI.h>         // for communication with Ethernet Shield
#include <Ethernet.h>    // for communication with NTP Server via UDP

// define the different pins
#define SOUNDPIN A2
#define DHTPIN 3
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#define LIGHTPIN A4
//Variables
char ssid[] = SECRET_SSID;        
char pass[] = SECRET_PASS;    
int status = WL_IDLE_STATUS;     // the Wifi radio's status

//70e3-69-17-239-181.ngrok.io
char serverAddress[] = " e881-69-17-239-181.ngrok.io";
int port = 80;
WiFiClient wifi;
HttpClient client = HttpClient(wifi,serverAddress,port);
String sound;
String lastSound; 
String temperature;
String humidity;
String light;
// setups the liquid crystal display
const int rs = 9, en = 10, d4 = 11, d5 = 12, d6 = 13, d7 = 14;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  
  Serial.begin(9600);
  while (!Serial);
while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
    
    // wait 10 seconds for connection:
    delay(5000);
}
Serial.println("You're connected to the network");

  Serial.println("----------------------------------------");
  printData();
  Serial.println("----------------------------------------");

  // Set input pins
  pinMode(SOUNDPIN,INPUT);
  pinMode(LIGHTPIN,INPUT);
  dht.begin();
}
void printData() {
  Serial.println("Board Information:");
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  Serial.println();
  Serial.println("Network Information:");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);
}

void loop() {

   // Read inputs from sensors
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  float s = analogRead(SOUNDPIN);
  float l = analogRead(LIGHTPIN);
  // Sound Logic
  if(s<=554 && s>=548){
    sound = "silent";
  } else if(s<=557 && s>=545){
    sound = "some sound";
  } else if(s<565 && s>533){
    sound = "big sound";
  } else {
    sound = "Loud";
  } 
  //Humidity Logic
  
  if(h>80){
    humidity = "Moist";
  } else if(h>60){
    humidity = "Humid";
  } else if(h>40){
    humidity = "Normal";
  } else if(h>20){
    humidity = "Dry";
  } else {
    humidity = "Desert";
  }
  //Light Logic
  
  if(l==1023) {
    light= "Strong light";
  } else if(l>800) {
    light= "luminous";
  } else if(l>600) {
    light= "Normal";
  } else if(l>300) {
    light= "faint";
  } else{
    light="Dark";
  }
    String postData;
    DynamicJsonDocument doc(1024);
    doc["temperature"] = (int)t;
    doc["humidity"]   = humidity;
    doc["brightness"] = light;
    doc["sound"] = sound;
    serializeJson(doc, postData);
    serializeJson(doc, Serial);
    String contentType = "application/json";
     Serial.println("\nMaking post request");
     
     client.beginRequest();
     //client.get("/sensors/450/sounds");
     client.post("/sensors/450/");
     client.sendHeader("Content-Type", "application/json");
     client.sendHeader("Content-Length", postData.length());
     client.sendHeader("authorization", "Bearer {2JEuuaC5Hj4kf2eMavkxIP1LrvA_6Zikiebi18T8xtHFrSaDc}");
     client.sendHeader("ngrok-version", "2");
     client.sendHeader("ngrok-skip-browser-warning", 1);
     client.beginBody();
     client.print(postData);
     client.endRequest();
    int statusCode = client.responseStatusCode();
    String response = client.responseBody();
     
    Serial.print("Status code: ");
    Serial.println(statusCode);
     
    Serial.print("Response: ");
    Serial.println(response);
  
  // waits 10 minutes
   delay(600000);
}
