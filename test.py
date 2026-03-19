import pigpio
import time

PIN = 19

NEUTRAL = 1500
MIN = 1100
MAX = 1900

def percent_to_pw(p):
    return int(NEUTRAL + p * (MAX - NEUTRAL))

pi = pigpio.pi('10.42.0.187')
assert pi.connected, "pigpio not connected"   # local pigpiod

if not pi.connected:
    raise RuntimeError("pigpio not connected")

# ---- ARM ESC ----
pi.set_servo_pulsewidth(PIN, NEUTRAL)
time.sleep(3)   # IMPORTANT

# ---- TEST SEQUENCE ----
sequence = [
    0.0,   # off
    0.2,   # 20%
    0.8,   # 80%
    0.4,   # 40%
    0.0    # off
]

for val in sequence:
    pw = percent_to_pw(val)
    pi.set_servo_pulsewidth(PIN, pw)
    time.sleep(1)

# ---- DISARM CLEANLY ----
pi.set_servo_pulsewidth(PIN, NEUTRAL)
time.sleep(2)

# release the pin
pi.set_servo_pulsewidth(PIN, 0)
pi.stop()
