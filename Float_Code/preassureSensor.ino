#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;

void setup() {
  Serial.begin(9600);
  delay(1000);

  Serial.println("Initializing BlueRobotics Depth/Pressure Sensor...");

  Wire.begin();  // SDA=A4, SCL=A5

  // Initialize
  if (!sensor.init()) {
    Serial.println("ERROR: Sensor not found! Check wiring.");
    while (1);
  }

  // Manually choose the model
  sensor.setModel(MS5837::MS5837_30BA);  
  // Alternatives:
  // sensor.setModel(MS5837::MS5837_02BA);
  // sensor.setModel(MS5837::MS5803_14BA);
  
  sensor.setFluidDensity(997); // fresh water

  Serial.println("Sensor initialized!");
}

void loop() {
  sensor.read();

  float pressure_mbar = sensor.pressure();
  float temp_C = sensor.temperature();
  float depth_m = sensor.depth();

  Serial.print("Pressure: ");
  Serial.print(pressure_mbar);
  Serial.print(" mbar | Temp: ");
  Serial.print(temp_C);
  Serial.print(" C | Depth: ");
  Serial.print(depth_m);
  Serial.println(" m");

  delay(500);
}
