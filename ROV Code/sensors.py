import pigpio
import struct
import math
import time
import threading

# ---------------- IMU ----------------
MPU9250_ADDR = 0x68
PWR_MGMT_1 = 0x6B
GYRO_XOUT_H = 0x43
ACCEL_XOUT_H = 0x3B

GYRO_SCALE = 131.0
ACCEL_SCALE = 16384.0

# ---------------- TSYS01 ----------------
TSYS01_ADDR = 0x77
TSYS01_RESET = 0x1E
TSYS01_START = 0x48
TSYS01_READ = 0x00


# =========================================================
# GLOBAL STATE
# =========================================================

pi = None
imu_handle = None
temp_handle = None

leak_pin = None

flags = {}
data = {}

gyro_offset = [0.0, 0.0, 0.0]

pitch = 0.0
roll = 0.0

alpha = 0.98
dt = 0.01

running = False
lock = threading.Lock()

threads = {}


# =========================================================
# INIT / QUIT
# =========================================================

def init(_leak_pin, raspi: pigpio.pi):
    global pi, imu_handle, temp_handle, leak_pin, running
    global flags, data, threads

    pi = raspi
    leak_pin = _leak_pin

    imu_handle = pi.i2c_open(1, MPU9250_ADDR)
    temp_handle = pi.i2c_open(1, TSYS01_ADDR)

    flags = {
        "piConnect": False,
        "controllerConnect": False,
        "cameraConnect": False,
        "leak": False
    }

    data = {
        "gyro": (0.0, 0.0),
        "temp": 0.0
    }

    running = True

    # leak pin setup
    pi.set_mode(leak_pin, pigpio.INPUT)
    pi.set_pull_up_down(leak_pin, pigpio.PUD_UP)
    pi.set_glitch_filter(leak_pin, 20000)

    # wake IMU
    pi.i2c_write_byte_data(imu_handle, PWR_MGMT_1, 0x00)
    time.sleep(0.1)

    # reset temp sensor
    pi.i2c_write_byte(temp_handle, TSYS01_RESET)
    time.sleep(0.1)

    # start threads
    threads["imu"] = threading.Thread(target=_imu_loop, daemon=True)
    threads["temp"] = threading.Thread(target=_temp_loop, daemon=True)
    threads["leak"] = threading.Thread(target=_leak_loop, daemon=True)

    threads["imu"].start()
    threads["temp"].start()
    threads["leak"].start()


def quit():
    global running

    running = False

    # wait for threads
    for t in threads.values():
        t.join(timeout=1.0)

    try:
        pi.i2c_close(imu_handle)
        pi.i2c_close(temp_handle)
        pi.stop()
    except:
        pass


# =========================================================
# IMU
# =========================================================

def read_gyro():
    count, d = pi.i2c_read_i2c_block_data(imu_handle, GYRO_XOUT_H, 6)
    if count == 6:
        gx, gy, gz = struct.unpack('>hhh', d)
        return (
            gx / GYRO_SCALE - gyro_offset[0],
            gy / GYRO_SCALE - gyro_offset[1],
            gz / GYRO_SCALE - gyro_offset[2]
        )
    return None


def read_accel():
    count, d = pi.i2c_read_i2c_block_data(imu_handle, ACCEL_XOUT_H, 6)
    if count == 6:
        ax, ay, az = struct.unpack('>hhh', d)
        return ax / ACCEL_SCALE, ay / ACCEL_SCALE, az / ACCEL_SCALE
    return None


def calibrate_gyro(samples=500):
    global gyro_offset

    sums = [0.0, 0.0, 0.0]

    for _ in range(samples):
        g = read_gyro()
        if g:
            sums[0] += g[0]
            sums[1] += g[1]
            sums[2] += g[2]
        time.sleep(0.002)

    gyro_offset = [s / samples for s in sums]


def _imu_loop():
    global pitch, roll

    while running:
        gyro = read_gyro()
        accel = read_accel()

        if gyro and accel:
            gx, gy, _ = gyro
            ax, ay, az = accel

            # integrate gyro
            pitch += gx * dt
            roll  += gy * dt

            # accel reference
            accel_pitch = math.degrees(math.atan2(ay, az))
            accel_roll  = math.degrees(math.atan2(-ax, az))

            # complementary filter
            pitch = alpha * pitch + (1 - alpha) * accel_pitch
            roll  = alpha * roll + (1 - alpha) * accel_roll

            with lock:
                data["gyro"] = (pitch, roll)

        time.sleep(dt)


# =========================================================
# TSYS01 TEMP SENSOR
# =========================================================

def _tsys01_read_raw():
    pi.i2c_write_byte(temp_handle, TSYS01_START)
    time.sleep(0.01)

    count, d = pi.i2c_read_i2c_block_data(temp_handle, TSYS01_READ, 3)
    if count == 3:
        return d[0] << 16 | d[1] << 8 | d[2]
    return None


def _temp_loop():
    while running:
        raw = _tsys01_read_raw()

        if raw:
            # simplified conversion (good enough for ROV monitoring)
            temp_c = -40.0 + 0.00002 * raw

            with lock:
                data["temp"] = temp_c

        time.sleep(0.2)  # TSYS01 doesn't need high rate


# =========================================================
# LEAK SENSOR
# =========================================================

def _leak_loop():
    while running:
        state = pi.read(leak_pin)

        with lock:
            flags["leak"] = bool(state)

        time.sleep(0.05)


# =========================================================
# UPDATE
# =========================================================

def update():
    # non-blocking snapshot access point
    with lock:
        gyro = data["gyro"]
        temp = data["temp"]
        leak = flags["leak"]

    return {
        "gyro": gyro,
        "temp": temp,
        "leak": leak
    }


#=========================================================
# FLAG API
# =========================================================


def setPiConnection(c: bool):
    flags["piConnect"] = c


def setControllerConnection(c: bool):
    flags["controllerConnect"] = c

def setCameraConnection(c: bool):
    flags["cameraConnect"] = c