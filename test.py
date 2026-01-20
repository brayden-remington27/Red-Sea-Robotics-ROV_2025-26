import pigpio
import time

RASPI_HOST = "192.168.2.1"
GPIO_PIN = 17  # BCM numbering

pi = pigpio.pi(RASPI_HOST)

if not pi.connected:
    print("Failed to connect to Raspberry Pi")
    exit(1)

pi.set_mode(GPIO_PIN, pigpio.OUTPUT)
pi.write(GPIO_PIN, 1)
print("GPIO 17 HIGH")

time.sleep(6)

pi.write(GPIO_PIN, 0)
print("GPIO 17 LOW")

pi.stop()
