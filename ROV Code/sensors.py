flags = {
    "piConnect": False,
    "controllerConnect": False
    #"LEAK_PIN": config.getint("GENERAL", "LEAK_PIN", fallback=5)
}  # TODO: I also need to set up a flag to detect pi connection
data = {
    "intTemp": 0,
    "extTemp": 0,
    "pressure": 0,
    "depth": 0
}

def setPiConnection(c: bool):
    flags["piConnect"] = c

def setControllerConnection(c: bool):
    flags["controllerConnect"] = c