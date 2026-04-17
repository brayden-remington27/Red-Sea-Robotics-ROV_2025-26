import pigpio
import time
import struct
import math
import pygame

MPU9250_ADDR = 0x68

PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
ACCEL_XOUT_H = 0x3B

GYRO_SCALE = 131.0
ACCEL_SCALE = 16384.0

pi = pigpio.pi('10.42.0.186')
if not pi.connected:
    exit()

handle = pi.i2c_open(1, MPU9250_ADDR)


# ---------------- IMU ----------------
gyro_offset = [0, 0, 0]

def read_gyro():
    count, data = pi.i2c_read_i2c_block_data(handle, GYRO_XOUT_H, 6)
    if count == 6:
        gx, gy, gz = struct.unpack('>hhh', data)
        return (
            gx / GYRO_SCALE - gyro_offset[0],
            gy / GYRO_SCALE - gyro_offset[1],
            gz / GYRO_SCALE - gyro_offset[2]
        )
    return None


def read_accel():
    count, data = pi.i2c_read_i2c_block_data(handle, ACCEL_XOUT_H, 6)
    if count == 6:
        ax, ay, az = struct.unpack('>hhh', data)
        return ax / ACCEL_SCALE, ay / ACCEL_SCALE, az / ACCEL_SCALE
    return None


def setup():
    pi.i2c_write_byte_data(handle, PWR_MGMT_1, 0x00)
    time.sleep(0.1)


def calibrate_gyro(samples=500):
    global gyro_offset

    print("Calibrating... keep sensor still")

    sums = [0, 0, 0]

    for _ in range(samples):
        count, data = pi.i2c_read_i2c_block_data(handle, GYRO_XOUT_H, 6)
        if count == 6:
            gx, gy, gz = struct.unpack('>hhh', data)
            sums[0] += gx / GYRO_SCALE
            sums[1] += gy / GYRO_SCALE
            sums[2] += gz / GYRO_SCALE
        time.sleep(0.002)

    gyro_offset = [s / samples for s in sums]

    print("Calibration done:", gyro_offset)


# ---------------- PYGAME ----------------
pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("ROV IMU")

font = pygame.font.SysFont(None, 36)

button_rect = pygame.Rect(120, 220, 160, 50)

# ---------------- MAIN ----------------
setup()

pitch = 0.0
roll = 0.0

alpha = 0.98
dt = 0.01

running = True

while running:
    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                calibrate_gyro()

    # --- IMU update ---
    gyro = read_gyro()
    accel = read_accel()

    if gyro and accel:
        gx, gy, gz = gyro
        ax, ay, az = accel

        pitch += gx * dt
        roll  += gy * dt

        accel_pitch = math.degrees(math.atan2(ay, az))
        accel_roll  = math.degrees(math.atan2(-ax, az))

        pitch = alpha * pitch + (1 - alpha) * accel_pitch
        roll  = alpha * roll  + (1 - alpha) * accel_roll

    # --- draw ---
    screen.fill((30, 30, 30))

    pitch_text = font.render(f"Pitch: {pitch:6.2f}", True, (255, 255, 255))
    roll_text  = font.render(f"Roll:  {roll:6.2f}", True, (255, 255, 255))

    screen.blit(pitch_text, (80, 80))
    screen.blit(roll_text,  (80, 130))

    # button
    pygame.draw.rect(screen, (70, 130, 180), button_rect)
    btn_text = font.render("Calibrate", True, (255, 255, 255))
    screen.blit(btn_text, (button_rect.x + 20, button_rect.y + 10))

    pygame.display.flip()

    time.sleep(dt)

pygame.quit()
pi.i2c_close(handle)
pi.stop()