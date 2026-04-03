def init():
    global out
    #TODO: This is a bit of a duplicate of the PINS dict in outputs.py, find some way to integrate together
    out = {
        "LEFT": 0.0,
        "RIGHT": 0.0,
        "SW": 0.0,
        "SE": 0.0,
        "NW": 0.0,
        "NE": 0.0,
        "ARM": 0.0,
        "CAMERA": 0.0
    }




def inToOutPercent(hat: tuple, axes: dict, max_scale: float, cam_speed: float):
    
    #AXIS:
    #   "lx": _
    #   "ly": _
    #   "rx": _
    #   "ry": _
    
    move = axes["ly"]
    turn = axes["rx"]
    profile = axes["ry"]
    
    ###### FRONTS ######
    
    # default tank tread movement, range from -2 to 2
    out["LEFT"] = move + turn
    out["RIGHT"] = move - turn
    
    # normalize defaults, -1 to 1
    max_mag = max(1.0, abs(out["LEFT"]), abs(out["RIGHT"]))
    out["LEFT"] /= max_mag
    out["RIGHT"] /= max_mag
    
    # scale to not burn out buck
    out["LEFT"] *= max_scale
    out["RIGHT"] *= max_scale
    
    
    ###### UP/DOWN ######
    
    # applies to all up/down motors ot just move up and down as ry says
    out["SW"] = profile*max_scale
    out["SE"] = profile*max_scale
    out["NW"] = profile*max_scale
    out["NE"] = profile*max_scale

   #TODO: add strafing


    ###### CAMERA SERVO ######
    
    if abs(out["CAMERA"]) <= max_scale:
        out["CAMERA"] += hat[1]*cam_speed
    else:
        out["CAMERA"] = (out["CAMERA"]/abs(out["CAMERA"]))*max_scale  #  +-0.99

    
    return out

#TODO: Unused currently
def remap(x, smin, smax, fmin, fmax):  # takes in a value and the values it ranges between, outputs that value along a different range
    return fmin + ((x - smin) * (fmax - fmin) / (smax - smin))