#include <WiFi.h>
#include <PubSubClient.h>

// On Rasp 
// mosquitto_sub -h localhost -t "sensor/light"

const char* ssid = "labs@fhv.at";     
const char* password = "vZDjRViutq9lSJ"; 
const char* mqtt_server = "172.21.64.93";  

WiFiClient espClient;
PubSubClient client(espClient);

int photoResistorPin = 2;  // GPIO where the photoresistor is connected
int sensorValue = 0;       // Variable to store the value from the sensor

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("WiFi connected");
}

void setup() {
  Serial.begin(115200);    // Start the serial communication
  pinMode(photoResistorPin, INPUT);  // Set the pin as input
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client")) {
      Serial.println("MQTT connected");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  sensorValue = analogRead(photoResistorPin);
  String payload = String(sensorValue);
  
  Serial.print("Light Intensity: ");
  Serial.println(sensorValue);

  client.publish("sensor/light", payload.c_str());  // Publish data to the topic

  delay(100);  // This is the most critical delay, defines how fast it sends data
}
