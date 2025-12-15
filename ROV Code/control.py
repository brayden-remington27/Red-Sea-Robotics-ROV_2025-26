import pigpio
pi = pigpio.pi('raspberrypi.local')   # or IP address of the Pi
pi.write(17, 0)
print(pi.connected)