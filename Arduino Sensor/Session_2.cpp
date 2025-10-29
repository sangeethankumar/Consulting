#include <Wire.h>
#include "SparkFun_SGP40_Arduino_Library.h"

SparkFun_SGP40 sgp;

const uint8_t muxAddresses[2] = { 0x70, 0x71 };
const uint8_t SGP40_ADDRESS = 0x59;

bool isSGP40Connected() {
  Wire.beginTransmission(SGP40_ADDRESS);
  return Wire.endTransmission() == 0;
}

void setup() {
  Wire.begin();
  Serial.begin(115200);
  while (!Serial);
}

void loop() {
  for (uint8_t mux = 0; mux < NUM_MUXES; mux++) {
    uint8_t muxAddr = muxAddresses[mux];

    for (uint8_t ch = 0; ch < 8; ch++) {
      Wire.beginTransmission(muxAddr);
      Wire.write(1 << ch); 
      Wire.endTransmission();
      delay(5);

      Serial.print("MUX 0x");
      Serial.print(muxAddr, HEX);
      Serial.print(" Channel ");
      Serial.print(ch);

      if (isSGP40Connected()) {
        Serial.println("SGP40 found");

        if (!sgp.begin()) {
          Serial.println("!!!Failed to initialize SGP40 sensor");
          continue;
        }

        int32_t vocIndex = sgp.getVOCindex();
        Serial.print("VOC Index: ");
        Serial.println(vocIndex);
      } else {
        Serial.println("!!!No sensor found");
      }
    }
  }

  delay(1000);
}
