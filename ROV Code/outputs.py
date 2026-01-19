def init(config):
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

    MAX_PW = config.getfloat("PWM", "MAX_PW", fallback=0.0019)
    MIN_PW = config.getfloat("PWM", "MIN_PW", fallback=0.0011)

def updateActivations(activations: dict):
    pass  # TODO: actually send the activations to Tyrone
