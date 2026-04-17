def init(config):
    global MAX_PERCENT
    MAX_PERCENT = config.getfloat("CONFIG", "MAX_PERCENT", fallback=0.8)
    global BUMP_SPEED
    BUMP_SPEED = config.getfloat("CONFIG", "BUMP_SPEED", fallback=0.07)
    
    global CAM_SPEED
    global ARM_SPEED
    CAM_SPEED = config.getfloat("CONFIG", "CAMERA_MOVE_SPEED", fallback=0.001)  # 0.1% per loop
    ARM_SPEED = config.getfloat("CONFIG", "ARM_MOVE_SPEED", fallback=0.001)  # 0.1% per loop
    
    global RAMP_SPEED
    RAMP_SPEED = config.getfloat("CONFIG", "OUTPUT_RAMP_SPEED", fallback=0.01)
    

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
    


# make sure that the motors don't max out too quickly, otherwise everyting crashes
def ramp_toward(current: float, target: float, max_delta: float) -> float:
    if target > current:
        return min(current + max_delta, target)
    if target < current:
        return max(current - max_delta, target)
    return current


# TODO: Maybe move all these variables to the init? some might change like max scale with different movement modes, but others wouldn't and could go to init
def inToOutPercent(hat: tuple, buttons: list, axes: dict, triggers: dict, limit: float):
    MAX_PERCENT = limit
    
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
    
    
    move = -axes["ly"]
    turn = axes["rx"]
    profile = axes["ry"]
    
    ###### FRONTS ######
    
    # default tank tread movement, range from -2 to 2
    targetLeft = move - turn
    targetRight = move + turn
    
    # normalize defaults, -1 to 1
    max_mag = max(1.0, abs(targetLeft), abs(targetRight))
    targetLeft /= max_mag  # these "target" values are just what it wants to set it to with no ramping, but...
    targetRight /= max_mag
    
    # scale to not burn out buck
    targetLeft *= MAX_PERCENT
    targetRight *= -MAX_PERCENT  # negated cuz some are counterclockwise
    
    if abs(targetLeft) > abs(out["LEFT"]) and abs(targetLeft) > MAX_PERCENT*0.8:  # only ramp if it's greater
        out["LEFT"] = ramp_toward(out["LEFT"], targetLeft, RAMP_SPEED)  # ... it gets ramped here to make sure it doesnt' crash
        out["SW"] =  ramp_toward(out["SW"], targetRight*0.4, RAMP_SPEED)
        out["NW"] =  -ramp_toward(out["NW"], targetRight*0.4, RAMP_SPEED)
    else:
        out["LEFT"] = targetLeft
    if abs(targetRight) > abs(out["RIGHT"]) and abs(targetRight) > MAX_PERCENT*0.8:
        out["RIGHT"] = ramp_toward(out["RIGHT"], targetRight, RAMP_SPEED)
        out["SE"] =  ramp_toward(out["SE"], targetRight*0.4, RAMP_SPEED)
        out["NE"] =  -ramp_toward(out["NE"], targetRight*0.4, RAMP_SPEED)
    else:
        out["RIGHT"] = targetRight
    
    
    ###### UP/DOWN ######
    
    # applies to all up/down motors ot just move up and down as ry says
    targetSW = profile*MAX_PERCENT
    targetSE = -profile*MAX_PERCENT
    targetNW = -profile*MAX_PERCENT
    targetNE = profile*MAX_PERCENT
    
    

   #TODO: add strafing
   #TODO: I added small bumps to the sides, as I don't have an IMU for strafing stabilization and shit

    # Bumps a little bit more to the motors sides when the hat is pressed
    if hat[0] == 1 or hat[1] == 1:
        targetSW = min(out["SW"]+BUMP_SPEED, MAX_PERCENT)
        targetNE = max(out["NE"]-BUMP_SPEED, -MAX_PERCENT)
    if hat[0] == -1 or hat[1] == 1:
        targetSE = max(out["SE"]-BUMP_SPEED, -MAX_PERCENT)
        targetNW = min(out["NW"]+BUMP_SPEED, MAX_PERCENT)
    if hat[0] == 1 or hat[1] == -1:
        targetNW = max(out["NW"]-BUMP_SPEED, -MAX_PERCENT)
        targetSE = min(out["SE"]+BUMP_SPEED, MAX_PERCENT)
    if hat[0] == -1 or hat[1] == -1:
        targetNE = min(out["NE"]+BUMP_SPEED, MAX_PERCENT)
        targetSW = max(out["SW"]-BUMP_SPEED, -MAX_PERCENT)
    

    out["SW"] = ramp_toward(out["SW"], targetSW, RAMP_SPEED)
    out["SE"] = ramp_toward(out["SE"], targetSE, RAMP_SPEED)
    out["NW"] = ramp_toward(out["NW"], targetNW, RAMP_SPEED)
    out["NE"] = ramp_toward(out["NE"], targetNE, RAMP_SPEED)

    ###### CAMERA SERVO ######
    # servo works at absolute positioning, pwm input = the amount here or there it's set to
    
    if abs(out["CAMERA"]) <= 1:  # I changed MAX_PERCENT for 1, cuz the servo isn't a burnout worry
        out["CAMERA"] += buttons[4]*CAM_SPEED
        out["CAMERA"] -= buttons[5]*CAM_SPEED
    else:
        out["CAMERA"] = (out["CAMERA"]/abs(out["CAMERA"]))*1  #  ±0.99
    
    
    ###### ARM ######
    # the arm works as constant velocity, the pwm input is how fast it opens or closes
    
    if abs(out["ARM"]) <= 1:
        # closes below 1470 µs
        # opens above 1530 µs
        out["ARM"] = (triggers["lt"]-triggers["rt"])*ARM_SPEED
    else:
        out["ARM"] = (out["ARM"]/abs(out["ARM"]))*1

    
    
    
    return out







#TODO: Unused currently
def remap(x, smin, smax, fmin, fmax):  # takes in a value and the values it ranges between, outputs that value along a different range
    return fmin + ((x - smin) * (fmax - fmin) / (smax - smin))