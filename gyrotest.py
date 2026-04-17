import pigpio
import time
import struct
import math

MPU9250_ADDR = 0x68

PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
ACCEL_XOUT_H = 0x3B

# Sensitivity (default settings)
GYRO_SCALE = 131.0      # LSB/(deg/s) for ±250 dps
ACCEL_SCALE = 16384.0   # LSB/g for ±2g

pi = pigpio.pi('10.42.0.186')
if not pi.connected:
    exit()

handle = pi.i2c_open(1, MPU9250_ADDR)


def read_gyro():
    count, data = pi.i2c_read_i2c_block_data(handle, GYRO_XOUT_H, 6)
    if count == 6:
        gx, gy, gz = struct.unpack('>hhh', data)
        return gx / GYRO_SCALE, gy / GYRO_SCALE, gz / GYRO_SCALE
    return None


def read_accel():
    count, data = pi.i2c_read_i2c_block_data(handle, ACCEL_XOUT_H, 6)
    if count == 6:
        ax, ay, az = struct.unpack('>hhh', data)
        return ax / ACCEL_SCALE, ay / ACCEL_SCALE, az / ACCEL_SCALE
    return None


def setup():
    # Wake up MPU
    pi.i2c_write_byte_data(handle, PWR_MGMT_1, 0x00)
    time.sleep(0.1)


# --- MAIN ---
setup()

# angles (degrees)
pitch = 0.0
roll = 0.0

alpha = 0.98   # gyro trust
dt = 0.05      # 100 Hz loop

print("Running IMU fusion... Ctrl+C to stop")

while True:
    gyro = read_gyro()
    accel = read_accel()

    if gyro and accel:
        gx, gy, gz = gyro
        ax, ay, az = accel

        # --- integrate gyro ---
        pitch += gx * dt
        roll  += gy * dt

        # --- accel angles (degrees) ---
        accel_pitch = math.degrees(math.atan2(ay, az))
        accel_roll  = math.degrees(math.atan2(-ax, az))

        # --- complementary filter ---
        pitch = alpha * pitch + (1 - alpha) * accel_pitch
        roll  = alpha * roll  + (1 - alpha) * accel_roll

        print(f"Pitch: {pitch:7.2f} | Roll: {roll:7.2f}")

    time.sleep(dt)