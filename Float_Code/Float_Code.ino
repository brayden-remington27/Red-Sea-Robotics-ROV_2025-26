#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;
//function for getting pressure - check
//function for taking pressure and estimating depth given temp and salinity
//function for taking necesary volume displacement given steps per ml of stepper motor (steps are global var)
//function for taking current difference in depth to target depth --> return volume of syringes that need to be displaced given global var about float (mass,max disp)

float[2][10] itenerary = [[0.4, 10], [2.5, 30], [0.4, 30], [2.5, 30], [0.4, 30]]
float DISPLACEMENT;  // volume of the float
float VOLUME; // volume of the syringes
float MASS; // of the float
int steps per ml

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600)
 
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

float getPressure(){
  sensor.read();

  return sensor.pressure();
}

//calculates accurate fluid density
float calcDensity(){

}

float steps = 0; //def later
float volDisp(float stepsReq){
  //volume to be displaced = required steps/steps per ml
  return stepsReq/steps;
}

void loop() {
  // put your main code here, to run repeatedly:
  float pressure_mbar = getPressure();

  Serial.print("Pressure: ")
  Serial.print(pressure_mbar)
}
