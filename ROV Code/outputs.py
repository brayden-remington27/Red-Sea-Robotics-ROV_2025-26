import pigpio
import sensors

def init(config):

    global PINS
    PINS = {
        "FRONT_LEFT_PIN": config.getint("THRUSTERS", "FRONT_LEFT_PIN", fallback=19),
        "FRONT_RIGHT_PIN": config.getint("THRUSTERS", "FRONT_RIGHT_PIN", fallback=16),
        "UP_BACKLEFT_PIN": config.getint("THRUSTERS", "UP_BACKLEFT_PIN", fallback=21),
        "UP_BACKRIGHT_PIN": config.getint("THRUSTERS", "UP_BACKRIGHT_PIN", fallback=20),
        "UP_FRONTLEFT_PIN": config.getint("THRUSTERS", "UP_FRONTLEFT_PIN", fallback=26),
        "UP_FRONTRIGHT_PIN": config.getint("THRUSTERS", "UP_FRONTRIGHT_PIN", fallback=6),

        "ARM_PIN": config.getint("GENERAL", "ARM_PIN", fallback=13),
        "CAMERA_PIN": config.getint("GENERAL", "CAMERA_PIN", fallback=25),
        "LEAK_PIN": config.getint("GENERAL", "LEAK_PIN", fallback=5)
    }
    global MAX_PW, MIN_PW, MID_PW
    MAX_PW = config.getint("PWM", "MAX_PW", fallback=1900)
    MIN_PW = config.getint("PWM", "MIN_PW", fallback=1100)
    MID_PW = config.getint("PWM", "MID_PW", fallback=1500)



    #global pi
    #pi = pigpio.pi(config.get("NETWORKING", "PI_IP", fallback='raspberrypi.local'))
    #assert pi.connected, "Pi not Connected"

    print(config.get("NETWORKING", "PI_IP", fallback='raspberrypi.local'))

    pi = pigpio.pi('10.42.0.91')
    assert pi.connected, "pigpio not connected"   # local pigpiod

    if not pi.connected:
        raise RuntimeError("pigpio not connected")

    if pi.connected:
        sensors.setPiConnection(True)  # transmit pi status to sensors, to then be picked up by control then draw
    else:
        sensors.setPiConnection(False)


def activationToPw(p):
    return int(MID_PW + p * (MAX_PW - MID_PW))

def sendActivations(activations: dict):
    pass  # TODO: actually send the activations to Tyrone
