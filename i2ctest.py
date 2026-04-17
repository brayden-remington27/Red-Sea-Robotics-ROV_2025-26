import pigpio

pi = pigpio.pi('10.42.0.186')

pigpio.exceptions = False

print("scanning for i2c devices")

for address in range(0x08, 0x78):
    handle = pi.i2c_open(1, address)

    if handle >= 0:
        result = pi.i2c_read_byte(handle)

        if result >= 0:
            print(f"device found @: 0x{address:02X}")

        pi.i2c_close  # always do this, remember

pi.stop()
print("scan complete")


# ok so it shows 0x68 (the mpu9250 gyrscope ith) and 0x77 (blue robotics fast response temperature sensor ibl)