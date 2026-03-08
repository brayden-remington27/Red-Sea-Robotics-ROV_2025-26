# Just functions. I didn't want to make this file, maybe I'll figure out a way to get rid of it later.

def sticks_to_percents(axes: dict):
    out = {
        "LEFT": 0.0,
        "RIGHT": 0.0,
        "SW": 0.0,
        "SE": 0.0,
        "NW": 0.0,
        "NE": 0.0
    }
    
    #AXIS:
    #   "lx": _
    #   "ly": _
    #   "rx": _
    #   "ry": _
    
    # FRONTS
    out["LEFT"] = remap(-axes["ly"] + min(axes["rx"]/2.0, 0), -1, 1, -0.8, 0.8)  # clamping it to |0.8| max thrust
    out["RIGHT"] = remap(-axes["ly"] - max(axes["rx"]/2.0, 0), -1, 1, -0.8, 0.8)
    #TODO: fix it so that it goes backwards when opposite is forward on turn
    
    #TODO: do the rest of the motors
    
    return out


def remap(x, smin, smax, fmin, fmax):  # takes in a value and the values it ranges between, outputs that value along a different range
    return fmin + ((x - smin) * (fmax - fmin) / (smax - smin))