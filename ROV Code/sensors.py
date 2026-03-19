import pigpio

flags = {
    "piConnect": False,
    "controllerConnect": False
    #"LEAK_PIN": config.getint("GENERAL", "LEAK_PIN", fallback=5)
}
data = {
    "intTemp": 0,
    "extTemp": 0,
    "pressure": 0,
    "depth": 0
}

def init(leak_pin, raspi: pigpio.pi):
    global leak
    leak = leak_pin

    global pi
    pi = raspi

    global flags
    global data

def update():
    pi

def setPiConnection(c: bool):
    flags["piConnect"] = c

def setControllerConnection(c: bool):
    flags["controllerConnect"] = c