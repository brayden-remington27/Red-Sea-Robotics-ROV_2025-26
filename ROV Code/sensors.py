import pigpio

flags = {
    "piConnect": False,
    "controllerConnect": False,
    "cameraConnect": False,
    "leak": False
}
data = {
    "intTemp": 0,
    "extTemp": 0,
    "pressure": 0,
    "depth": 0
}

def init(_leak_pin, raspi: pigpio.pi):
    global leak_pin
    leak_pin = _leak_pin

    global pi
    pi = raspi

    global flags
    global data
    
    
    pi.set_mode(leak_pin, pigpio.INPUT)  # get digital input from the leak pin (5 usually)
    pi.set_pull_up_down(leak_pin, pigpio.PUD_UP)  # default state for the detector is high (pud_up)
    pi.set_glitch_filter(leak_pin, 20000)  # any fluctuation less than 20ms isn't counted

def update():
    #print(pi.read(leak_pin))
    flags["leak"] = pi.read(leak_pin)  # since I regestered the default as true I don't need to invert it even though 
    # the pin itself is constantly giving 1 if dry and 0 if wet

def setPiConnection(c: bool):
    flags["piConnect"] = c

def setControllerConnection(c: bool):
    flags["controllerConnect"] = c