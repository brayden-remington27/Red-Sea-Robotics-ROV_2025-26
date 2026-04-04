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




def inToOutPercent(hat: tuple, axes: dict, triggers: dict, max_scale: float, cam_speed: float, arm_speed: float):
    #HAT:
    #    (±_, ±_)
    
    #AXIS:
    #   "lx": ±_
    #   "ly": ±_
    #   "rx": ±_
    #   "ry": ±_
    
    #TRIGGERS:
    #    "lt": +_
    #    "rt": +_
    
    
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
    # servo works at absolute positioning, pwm input = the amount here or there it's set to
    
    if abs(out["CAMERA"]) <= 1:  # I changed max_scale for 1, cuz the servo isn't a burnout worry
        out["CAMERA"] += hat[1]*cam_speed
    else:
        out["CAMERA"] = (out["CAMERA"]/abs(out["CAMERA"]))*1  #  ±0.99
    
    
    ###### ARM ######
    # the arm works as constant velocity, the pwm input is how fast it opens or closes
    
    if abs(out["ARM"]) <= 1:
        # closes below 1470 µs
        # opens above 1530 µs
        out["ARM"] = triggers["lt"]-triggers["rt"]

    
    return out

#TODO: Unused currently
def remap(x, smin, smax, fmin, fmax):  # takes in a value and the values it ranges between, outputs that value along a different range
    return fmin + ((x - smin) * (fmax - fmin) / (smax - smin))