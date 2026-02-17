import pigpio
import sensors
import time

def percentToPWM(p):  # turns the percent value to a 1100–1900 clamped
    p = max(-1.0, min(1.0, 0))  # clamp
    if p >= 0:
        return int(MID_PW + p * (MAX_PW - MID_PW))
    else:
        return int(MID_PW + p * (MID_PW - MIN_PW))



def init(config):

    global pi
    global PINS
    PINS = {
        "FRONT_LEFT_PIN": config.getint("THRUSTERS", "FRONT_LEFT_PIN", fallback=19),
        "FRONT_RIGHT_PIN": config.getint("THRUSTERS", "FRONT_RIGHT_PIN", fallback=16),
        "UP_BACKLEFT_PIN": config.getint("THRUSTERS", "UP_BACKLEFT_PIN", fallback=21),
        "UP_BACKRIGHT_PIN": config.getint("THRUSTERS", "UP_BACKRIGHT_PIN", fallback=20),
        "UP_FRONTLEFT_PIN": config.getint("THRUSTERS", "UP_FRONTLEFT_PIN", fallback=26),
        "UP_FRONTRIGHT_PIN": config.getint("THRUSTERS", "UP_FRONTRIGHT_PIN", fallback=6),

        "ARM_PIN": config.getint("GENERAL", "ARM_PIN", fallback=13),
        "CAMERA_PIN": config.getint("GENERAL", "CAMERA_PIN", fallback=25)
    }
    global MAX_PW, MIN_PW, MID_PW
    MAX_PW = config.getint("PWM", "MAX_PW", fallback=1900)
    MIN_PW = config.getint("PWM", "MIN_PW", fallback=1100)
    MID_PW = config.getint("PWM", "MID_PW", fallback=1500)

    print(config.get("NETWORKING", "PI_IP", fallback='raspberrypi.local'))

    pi = pigpio.pi('10.42.0.91')
    #pi = pigpio.pi(config.get("NETWORKING", "PI_IP", fallback='raspberrypi.local'))
    assert pi.connected, "pigpio not connected"   # local pigpiod
    if not pi.connected: raise RuntimeError("pigpio Not Connected")

    if pi.connected: sensors.setPiConnection(True)  # transmit pi status to sensors, to then be picked up by control then draw
    else: sensors.setPiConnection(False)
    
    
    
    # make sure to arm
    print("Arming ESCs/Motors")
    for pin in PINS.values(): pi.set_servo_pulsewidth(pin, MID_PW)
    time.sleep(3)  # needs some time after being sent inputs
    print("ESCs Armed")




def sendActivations(percents: dict):
    if pi is None: return  # make sure
    
    for name, percent in percents.items():
        if name not in PINS:  # make sure
            continue

        pin = PINS[name]
        pwm = percentToPWM(percent)
        pi.set_servo_pulsewidth(pin, pwm)




def quit():
    global pi
    
    print("Stopping motors")

    if pi is None:
        return
    
    for pin in PINS.values():
        pi.set_servo_pulsewidth(pin, MID_PW)

    time.sleep(2)

    for pin in PINS.values():
        pi.set_servo_pulsewidth(pin, 0)

    pi.stop()
    pi = None
