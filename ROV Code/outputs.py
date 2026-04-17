import pigpio
import sensors
import time
import configparser  # not sure if needed
import IO


def percentToPWM(p, clamp: float):  # turns the percent value to a 1100–1900 clamped
    #TODO: not a todo, just saying this clamps even if the joysticks go beyond

    # N of times I forgot to include p within this function so it just returned a constant value: 2; something something nickle
    p = max(-clamp, min(clamp, p))  # barbaric clamp, physically doesn't let it go beyond
    if p >= 0:
        return int(MID_PW + p * (MAX_PW - MID_PW))
    else:
        return int(MID_PW + p * (MID_PW - MIN_PW))



def init(config, raspi: pigpio.pi):
    global pi
    pi = raspi

    global PINS
    # Map logical motor names used by control.py to config pin settings
    PINS = {
        # horizontal/front thrusters
        "LEFT": config.getint("THRUSTERS", "LEFT", fallback=19),
        "RIGHT": config.getint("THRUSTERS", "RIGHT", fallback=16),

        # vertical/up thrusters mapped to quadrant names
        # front = N, back = S, left = W, right = E
        "NW": config.getint("THRUSTERS", "NW", fallback=26),
        "NE": config.getint("THRUSTERS", "NE", fallback=6),
        "SW": config.getint("THRUSTERS", "SW", fallback=21),
        "SE": config.getint("THRUSTERS", "SE", fallback=20),

        # other devices
        "ARM": config.getint("GENERAL", "ARM", fallback=13),
        "CAMERA": config.getint("GENERAL", "CAMERA", fallback=25)  # camera servo
    }
    global MAX_PW, MIN_PW, MID_PW
    MAX_PW = config.getint("PWM", "MAX_PW", fallback=1900)
    MIN_PW = config.getint("PWM", "MIN_PW", fallback=1100)
    MID_PW = config.getint("PWM", "MID_PW", fallback=1500)

    global MAX_PERCENT
    MAX_PERCENT = config.getfloat("CONFIG", "MAX_PERCENT", fallback=0.8)

    PI_IP = config.get("NETWORKING", "PI_IP", fallback='raspberrypi.local')
    
    
    if not pi.connected: raise RuntimeError("pigpio Not Connected")

    if pi.connected: sensors.setPiConnection(True)  # transmit pi status to sensors, to then be picked up by control then draw
    else: sensors.setPiConnection(False)
    
    
    
    # make sure to arm
    print("Arming ESCs/Motors")
    for pin in PINS.values(): 
        pi.set_servo_pulsewidth(pin, MID_PW)
    time.sleep(3)  # needs some time after being sent inputs
    print("ESCs Armed")




def sendActivations(percents: dict):
    #print(percents)

    if pi is None:
        return  # make sure, if there isn't a pi don't try to send

    displayPercents = {}
    for name, percent in percents.items():
        key = name if name in PINS else name.upper()  # the key that will be sought by the declaration of the pin is the name given by the dict of percents, uppercase if not there naturally
        if key not in PINS:
            continue

        pin = PINS[key]
        pwm = percentToPWM(percent, 1)
        if name[0] == 'L' or name[0] == 'R' or name[0] == 'N' or name[0] == 'S':
            percent *= MAX_PERCENT
            pwm = percentToPWM(percent, MAX_PERCENT)  # final clamping to ensure nothing is beyond 80%
            displayPercents[name] = percent
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
