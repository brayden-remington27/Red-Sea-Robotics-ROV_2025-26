import pigpio
import time

RASPI_HOST = "10.42.0.2"
MOTOR_PIN = 26

# Pulse widths in microseconds
MIN_PW = 1100
MAX_PW = 1900

def set_speed(pi, percent):
    """
    percent: 0.0 to 1.0
    """
    if percent <= 0:
        pi.set_servo_pulsewidth(MOTOR_PIN, 0)
        return

    pulse = MIN_PW + percent * (MAX_PW - MIN_PW)
    pi.set_servo_pulsewidth(MOTOR_PIN, pulse)

pi = pigpio.pi(RASPI_HOST)

if not pi.connected:
    raise RuntimeError("Failed to connect to Raspberry Pi")

pi.set_mode(MOTOR_PIN, pigpio.OUTPUT)

# OFF
set_speed(pi, 0.0)
time.sleep(1)

# 20%
set_speed(pi, 0.20)
time.sleep(1)

# 80%
set_speed(pi, 0.80)
time.sleep(1)

# 40%
set_speed(pi, 0.40)
time.sleep(1)

# OFF
set_speed(pi, 0.0)
time.sleep(1)

pi.stop()