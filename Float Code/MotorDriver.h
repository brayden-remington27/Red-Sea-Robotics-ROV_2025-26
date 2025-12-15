#ifndef MOTORDRIVER_H
#define MOTORDRIVER_H

class MotorDriver{
  private:

  public:
    void halt();
    void begin(double f);
    void rotateT(double f, double t);
    void rotate(double f, double n);
};

#endif