import pigpio
import time

PI_IP = "10.42.0.91"
GPIO = 26

MIN_PW = 1100   # off / minimum
MAX_PW = 1900   # max

pi = pigpio.pi(PI_IP)
assert pi.connected, "pigpio not connected"

print("OFF")
pi.set_servo_pulsewidth(GPIO, MIN_PW)
time.sleep(1)

print("20%")
pw_20 = MIN_PW + 0.2 * (MAX_PW - MIN_PW)
pi.set_servo_pulsewidth(GPIO, int(pw_20))
time.sleep(1)

print("80%")
pw_80 = MIN_PW + 0.8 * (MAX_PW - MIN_PW)
pi.set_servo_pulsewidth(GPIO, int(pw_80))
time.sleep(1)

print("40%")
pw_40 = MIN_PW + 0.4 * (MAX_PW - MIN_PW)
pi.set_servo_pulsewidth(GPIO, int(pw_40))
time.sleep(1)

print("OFF")
pi.set_servo_pulsewidth(GPIO, 0)  # IMPORTANT: 0 disables pulses

pi.stop()
