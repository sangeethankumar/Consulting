#include <DHT.h>
#include <Wire.h>

// Pin Definitions
#define DHTPIN 2
#define DHTTYPE DHT22
#define MQ2PIN A0

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  delay(500);
}

void loop() {
  // Read humidity and temperature from DHT22
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Read gas level from MQ2
  int gasValue = analogRead(MQ2PIN);

  // Check if any reads failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" deg C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  Serial.print("Gas: ");
  Serial.println(gasValue);

  // Wait before next reading
  delay(500);
}
