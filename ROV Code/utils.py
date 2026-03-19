# Just functions that don't apply to any file specifically. I didn't want to make this file, maybe I'll figure out a way to get rid of it later.

def sticks_to_percents(axes: dict, max_scale = 0.8):
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
    
    
    #TODO: do the rest of the motors
    ###### UP/DOWN ######
    
    # applies to all up/down motors ot just move up and down as ry says
    out["SW"] = profile*max_scale
    out["SE"] = profile*max_scale
    out["NW"] = profile*max_scale
    out["NE"] = profile*max_scale
    
    return out


def remap(x, smin, smax, fmin, fmax):  # takes in a value and the values it ranges between, outputs that value along a different range
    return fmin + ((x - smin) * (fmax - fmin) / (smax - smin))