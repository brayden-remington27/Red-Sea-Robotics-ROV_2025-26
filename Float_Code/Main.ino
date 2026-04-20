#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;

// -------- CONFIG --------

// logging
const int MAX_LOG = 200;
float depthLog[MAX_LOG];
unsigned long timeLog[MAX_LOG];
int logIndex = 0;

// control
float stepsPerML = 13.5;

// itinerary modes
#define MODE_DEPTH 0
#define MODE_SPEED 1

// itinerary: {mode, target, hold_time}
// MODE_DEPTH → target = depth (m)
// MODE_SPEED → target = velocity (m/s)
float itinerary[][3] = {
  {MODE_DEPTH, 0.5, 10},
  {MODE_SPEED, 0.1, 0},   // descend at 0.1 m/s
  {MODE_DEPTH, 2.0, 20},
  {MODE_SPEED, -0.1, 0},  // ascend
  {MODE_DEPTH, 0.5, 10}
};

const int itineraryLength = sizeof(itinerary) / sizeof(itinerary[0]);

// system state
int currentStep = 0;
unsigned long holdStart = 0;

// -------- SENSOR --------

float getDepth() {
  sensor.read();
  return sensor.depth();
}

// -------- LOGGING --------

void logData(float depth) {
  if (logIndex < MAX_LOG) {
    depthLog[logIndex] = depth;
    timeLog[logIndex] = millis();
    logIndex++;
  } else {
    // shift left (simple rolling buffer)
    for (int i = 1; i < MAX_LOG; i++) {
      depthLog[i - 1] = depthLog[i];
      timeLog[i - 1] = timeLog[i];
    }
    depthLog[MAX_LOG - 1] = depth;
    timeLog[MAX_LOG - 1] = millis();
  }
}

// compute vertical speed (m/s)
float getSpeed() {
  if (logIndex < 2) return 0;

  int i = logIndex - 1;
  float dz = depthLog[i] - depthLog[i - 1];
  float dt = (timeLog[i] - timeLog[i - 1]) / 1000.0;

  if (dt == 0) return 0;

  return dz / dt;
}

// -------- ACTUATION --------

// placeholder: replace with your stepper control
void applyVolumeChange(float vol) {
  int steps = vol * stepsPerML;

  // TODO: drive motor here
  // stepMotor(steps);

  Serial.print("Steps: ");
  Serial.println(steps);
}

// -------- CONTROL --------

// depth stabilization (P controller)
void controlDepth(float targetDepth) {
  float currentDepth = getDepth();
  float error = targetDepth - currentDepth;

  float Kp = 0.8;
  float volumeCmd = Kp * error;

  applyVolumeChange(volumeCmd);
}

// velocity stabilization (P controller)
void controlSpeed(float targetSpeed) {
  float currentSpeed = getSpeed();
  float error = targetSpeed - currentSpeed;

  float Kp = 1.5;
  float volumeCmd = Kp * error;

  applyVolumeChange(volumeCmd);
}

// -------- SETUP --------

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (!sensor.init()) {
    Serial.println("Sensor error!");
    while (1);
  }

  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(997);

  Serial.println("System ready");
}

// -------- LOOP --------

void loop() {
  float depth = getDepth();
  logData(depth);

  float speed = getSpeed();

  // current itinerary item
  int mode = itinerary[currentStep][0];
  float target = itinerary[currentStep][1];
  float holdTime = itinerary[currentStep][2];

  Serial.print("Depth: ");
  Serial.print(depth);
  Serial.print(" | Speed: ");
  Serial.print(speed);
  Serial.print(" | Step: ");
  Serial.println(currentStep);

  // ---- MODE HANDLING ----

  if (mode == MODE_DEPTH) {
    controlDepth(target);

    float tolerance = 0.05;

    if (abs(depth - target) < tolerance) {
      if (holdStart == 0) holdStart = millis();

      if ((millis() - holdStart) > holdTime * 1000) {
        currentStep++;
        holdStart = 0;
      }
    } else {
      holdStart = 0;
    }
  }

  else if (mode == MODE_SPEED) {
    controlSpeed(target);

    // stop when we reach next depth target
    float nextDepth = 0;

    // find next depth-type step
    for (int i = currentStep + 1; i < itineraryLength; i++) {
      if (itinerary[i][0] == MODE_DEPTH) {
        nextDepth = itinerary[i][1];
        break;
      }
    }

    // check if we've crossed or reached it
    if ((target > 0 && depth >= nextDepth) ||
        (target < 0 && depth <= nextDepth)) {
      currentStep++;
    }
  }

  // loop itinerary
  if (currentStep >= itineraryLength) {
    currentStep = 0;
  }

  delay(200);
}