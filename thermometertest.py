import pigpio
import time

# I2C settings
I2C_BUS = 1
I2C_ADDR = 0x77

# Initialize pigpio
pi = pigpio.pi('10.42.0.186')
if not pi.connected:
    raise RuntimeError("Could not connect to pigpio daemon. Run: sudo pigpiod")

# Open I2C connection
handle = pi.i2c_open(I2C_BUS, I2C_ADDR)

# Example: MS5837 / similar Blue Robotics sensor commands
CMD_RESET = 0x1E
CMD_ADC_READ = 0x00
CMD_CONVERT_D1 = 0x48  # Pressure (OSR=4096)
CMD_CONVERT_D2 = 0x58  # Temperature (OSR=4096)

def reset_sensor():
    pi.i2c_write_byte(handle, CMD_RESET)
    time.sleep(0.01)

def read_adc(cmd):
    pi.i2c_write_byte(handle, cmd)
    time.sleep(0.01)  # conversion time (adjust for speed vs accuracy)
    count, data = pi.i2c_read_i2c_block_data(handle, CMD_ADC_READ, 3)
    if count != 3:
        raise RuntimeError("Failed to read ADC")
    value = data[0] << 16 | data[1] << 8 | data[2]
    return value

def read_temperature_raw():
    return read_adc(CMD_CONVERT_D2)

def main():
    reset_sensor()

    while True:
        temp_raw = read_temperature_raw()
        print(f"Raw temperature: {temp_raw}")
        
        # NOTE:
        # To get actual °C, you must apply calibration coefficients (PROM read)
        # This example focuses on fast acquisition only
        
        time.sleep(0.05)  # ~20 Hz sampling

try:
    main()

except KeyboardInterrupt:
    print("Stopping...")

finally:
    pi.i2c_close(handle)
    pi.stop()