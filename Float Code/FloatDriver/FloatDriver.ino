//#include <arduino.h>

// start hovering for 5 sec, decend to 10m for 5 seconds, then rise to 0.5m (just below ice) and stay there for a while
float instructions[][2] = {{0.0, 5.0},{10.0, 5},{0.5, 999.0}};  // this is the list of depths (m) and the time period to stay there (s)
float moveSpeed = 0.5;  // the speed at which to decend to the specified depths (m/s)


// Physical constants
constexpr float GRAVITY = 9.80665f; // m/s^2
// Float properties (fill in)
constexpr float FLOAT_VOLUME = 0.0f;  // m^3 (external displaced volume)
constexpr float FLOAT_DRY_MASS = 0.0f;  // kg (no ballast)
constexpr float BALLAST_MAX_VOLUME = 0.0f;  // m^3 (max internal water volume)
// Hydrodynamics
constexpr float DRAG_COEF = 0.0f;
constexpr float CROSS_SECTION_AREA = 0.0f;  // m^2
// limits if needed
constexpr float MIN_FILL = 0.0f;  // %
constexpr float MAX_FILL = 1.0f;  // %



















class MotorDriver{
  private:

  public:

    void halt(){  // Cuts all movement of the motor

    }

    void begin(float f){  // start rotating
      
    }

    void rotateT(float f, float t){  // spin for a period of time

    }

    void rotate(float f, float n){  // rotate n times

    }

};

class ActuatorDriver : private MotorDriver{
  public:
    void move(float vel){  // extends the acutator at vel cm/s, positive for out negative for in

    }

    void extend(float cm){  // move in or out cm amout

    }

    void displace(float ml){ // displace ml of air/water

    }

    void fill(float percent){ // set replacement of % of air for water

    }
};

class AntennaeDriver{
  private:

  public:

  void halt(){

  }

  void begin(){
    
  }

};

class PressureDriver{
  private:

  public:
  float sampling_period = 0.1;

  PressureDriver::PressureDriver();

  void halt(){

  }

  void begin(){
    
  }

  float get_pressure(){

  }

  float get_density(){
    
  }

  float get_depth(){
    
  }

  float depth_difference(){
    
  }
};









// GLOBALS
float buoyantForce;
float currentSpeed;
float dragForce;
float fill;  // the amount of the balast that is water vs air (%)
float requiredMass;
float ballastWaterMassMax;
float requiredBallastMass;

// INSTANCES
PressureDriver manometer;
ActuatorDriver syringe;


void setup() {
  manometer.begin();

}

void quit(){
  exit(0);
}

float clamp(float x, float minVal, float maxVal){
  if (x < minVal) return minVal;
  if (x > maxVal) return maxVal;
  return x;
}

float computeBuoyantForce(float waterDensity){
  // F_b = rho * g * V
  return waterDensity * GRAVITY * FLOAT_VOLUME;
}

// get the drag force acting upon the float given current density and velocity of float
float computeDragForce(float waterDensity, float velocity){
  // Quadratic drag
  // F_d = 0.5 * rho * Cd * A * v^2
  return 0.5f * waterDensity * DRAG_COEF * CROSS_SECTION_AREA * velocity * velocity;
}

// get the requierd total mass of the float to have a terminal velocity of moveSpeed
float computeRequiredTotalMass(float waterDensity){
  buoyantForce = computeBuoyantForce(waterDensity);
  dragForce = computeDragForce(waterDensity, moveSpeed);

  // At terminal velocity:
  // F_b - m*g = F_d   (rising)
  // m = (F_b - F_d) / g

  // I need the net forces divided by acceleration (the mass) such that the float will have a speed
  return (buoyantForce - dragForce) / GRAVITY;
}

// get the percentage of the ballast that needs to be filled given the required total and the water density
float computeBallastFillFraction(float waterDensity){
  float requiredTotalMass = computeRequiredTotalMass(waterDensity);

  ballastWaterMassMax = BALLAST_MAX_VOLUME * waterDensity;

  requiredBallastMass = requiredTotalMass - FLOAT_DRY_MASS;

  fill = requiredBallastMass / ballastWaterMassMax;

  // I take in the required total mass and the density of the water that I will be drawing from
  // to get the fill percentage of the float needed
  return clamp(fill, MIN_FILL, MAX_FILL);
}



void loop() {
  // required mass for achieving the target speed
  requiredMass = computeRequiredTotalMass(manometer.get_density());

  // set the syringe to fill with the calculater
  syringe.fill(computeBallastFillFraction(manometer.get_density()));
  // what fill to set the balast to to get the bouyancy force to get a movement speed equal to the moveSpeed
  // we need to calculate the fill such that the terminal velocity is 0.5 m/s
}
