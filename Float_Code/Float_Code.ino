#include <Wire.h>
#include "MS5837.h"
#include <TimeLib.h>

MS5837 sensor;
float stepsPerML = 13.5;
float itinerary[5][2] = { //fixed this array
  {0.4, 10},
  {2.5, 30},
  {0.4, 30},
  {2.5, 30},
  {0.4, 30}
}; //[depth, duration] (depth in meters, duration in seconds)
float DISPLACEMENT;  // volume of the float
float VOLUME; // volume of the syringes
float MASS; // of the float
int MODE = 0;

float currentDepth = 0;
float prevDepth = 0; 

float currentVelocity = 0;
float prevVelocity = 0;
int targetItinerary = 0;

unsigned long previousMillis = 0;
const long interval = 100; // timestep in milliseconds (eg 10hz)

unsigned long startMillis;
//function for getting pressure - check
//function for taking pressure and estimating depth given temp and salinity
//function for taking necesary volume displacement given steps per ml of stepper motor (steps are global var)
//function for taking current difference in depth to target depth --> return volume of syringes that need to be displaced given global var about float (mass,max disp)

void setup() {
  // put your setup code here, to run once:
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

  startMillis = millis(); 

  Serial.println("Sensor initialized!");
}

float getPressure(){
  sensor.read();

  return sensor.pressure();
}

//calculates depth
float getDepth(){
  sensor.read();

  return sensor.depth();
}

float getTemp(){
  sensor.read();

  return sensor.temperature();
}

//necesary steps given volume & steps per ml of stepper motor
float stepsReq(float vol){
  //volume to be displaced = required steps/steps per ml
  return (int)vol * stepsPerML;
  
}

float volDisp(float targetDepth){
    float depth_m = getDepth();
    float diffDepth = targetDepth - depth_m;
    
    return 0.5*diffDepth;
}


void loop() {
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  //this is just reformatted with chatgpt, code is same I just wanted to make sure everything is in the right place
   if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Read sensor once
    sensor.read();
    currentDepth = sensor.depth();

    currentVelocity = (currentDepth - prevDepth) / (interval / 1000.0);

    float targetDepth = itinerary[targetItinerary][0];
    float targetTime = itinerary[targetItinerary][1];

    unsigned long timeElapsed = currentMillis - startMillis;

    Serial.print("Depth: ");
    Serial.print(currentDepth);
    Serial.print(" | Target: ");
    Serial.println(targetDepth);
    
    if (MODE == 0){
      //have stabalise position using depth below or above adjust depth
      //if its below or belowand speed is in the target direction dont move plunger
      // if not in target depth and speed is not in right direction, move plunger in the right direction
      // if timer is up mode = 1
        // timer: if starttime-currenttime == itinerar[target][1]*1000
        // starttime = current time
        // Simple proportional control
      float volume = volDisp(targetDepth); // volume of syringes (?)
      float steps = stepsReq(volume); //steps needed to move syringe

      if (timer == itinerary[targetItenerary][1]*1000){
        startMillis = currentMillis;
        targetItinerary ++;
        if (timeElapsed >= targetTime * 1000) {
        startMillis = currentMillis;
        targetItinerary++;

          if (targetItinerary >= 5) {
            targetItinerary = 0; //loops back to start
          }
          MODE = 1;
      }
    } else if (MODE == 1) {
      //if depth = targetdepth of current intirerayy pos change mode to stay
      if (currentDepth == targetDepth){
        mode = 0;
      }
      }
    prevDepth = currentDepth;
    prevVelocity = currentVelocity
  }
}

//2 modes --> move and stay
//start at beginning of itenerary, if current depth != depth in iterneary--> mode is move, if mode = move take target depth from itenerary
//compare vs current depth keep mode as move
//if speed != target speed (current - prev disp/time of loop) then increase or decrease fluid in syringe until current = target speed
//stay use depth, move use speed
//at the end set prev to current


