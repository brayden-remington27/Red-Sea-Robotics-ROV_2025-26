import pigpio
pi = pigpio.pi('10.42.0.91')
pi.write(17, 0)
print(pi.connected)