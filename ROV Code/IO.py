# -------------------------------------------------------
# GLOBALS
# -------------------------------------------------------

level_offset = [0.0, 0.0]

out = {}
target = {}


# -------------------------------------------------------
# INIT
# -------------------------------------------------------

def init(config):
    global BUMP_SPEED, CAM_SPEED, ARM_SPEED, RAMP_SPEED

    BUMP_SPEED = config.getfloat("CONFIG", "BUMP_SPEED", fallback=0.07)
    CAM_SPEED = config.getfloat("CONFIG", "CAMERA_MOVE_SPEED", fallback=0.001)
    ARM_SPEED = config.getfloat("CONFIG", "ARM_MOVE_SPEED", fallback=0.001)
    RAMP_SPEED = config.getfloat("CONFIG", "OUTPUT_RAMP_SPEED", fallback=0.01)

    global out, target

    motors = ["LEFT", "RIGHT", "SW", "SE", "NW", "NE", "ARM", "CAMERA"]

    out = {m: 0.0 for m in motors}
    target = {m: 0.0 for m in motors}


# -------------------------------------------------------
# CALIBRATION (SET CURRENT ORIENTATION AS LEVEL)
# -------------------------------------------------------

def calibrate_level(sensors):
    global level_offset
    pitch, roll = sensors["gyro"]
    level_offset = [pitch, roll]


# -------------------------------------------------------
# RAMP FUNCTION
# -------------------------------------------------------

def ramp_toward(current: float, target: float, max_delta: float) -> float:
    if target > current:
        return min(current + max_delta, target)
    if target < current:
        return max(current - max_delta, target)
    return current


# -------------------------------------------------------
# NORMALIZATION (PRESERVE RATIOS, LIMIT TO ±1)
# -------------------------------------------------------

def normalize_group(values: dict):
    max_mag = max(1.0, *(abs(v) for v in values.values()))
    return {k: v / max_mag for k, v in values.items()}


# -------------------------------------------------------
# MAIN CONTROL FUNCTION
# -------------------------------------------------------

def inToOutPercent(hat, buttons, axes, triggers, sensors):
    global out, target

    # ---------------------------
    # CONTROLLER INPUTS
    # ---------------------------
    move = -axes["ly"]
    turn = axes["rx"]
    vertical = axes["ry"]

    # ---------------------------
    # TANK DRIVE
    # ---------------------------
    left = move - turn
    right = move + turn

    max_mag = max(1.0, abs(left), abs(right))
    left /= max_mag
    right /= max_mag

    target["LEFT"] = left
    target["RIGHT"] = right

    # ---------------------------
    # IMU (WITH CALIBRATION OFFSET)
    # ---------------------------
    raw_pitch, raw_roll = sensors["gyro"]

    pitch = raw_pitch - level_offset[0]
    roll  = raw_roll  - level_offset[1]

    # tuning gains (you will tweak these)
    pitch_gain = -pitch * 0.005
    roll_gain  = -roll  * 0.005

    # ---------------------------
    # VERTICAL THRUSTERS
    # ---------------------------
    base_up = vertical

    sw = base_up + pitch_gain + roll_gain
    se = -base_up + pitch_gain - roll_gain
    nw = -base_up - pitch_gain + roll_gain
    ne = base_up - pitch_gain - roll_gain

    verticals = {
        "SW": sw,
        "SE": se,
        "NW": nw,
        "NE": ne
    }

    # normalize so nothing exceeds ±1
    verticals = normalize_group(verticals)

    target.update(verticals)

    # ---------------------------
    # CAMERA
    # ---------------------------
    target["CAMERA"] = out["CAMERA"] + buttons[4]*CAM_SPEED - buttons[5]*CAM_SPEED

    # ---------------------------
    # ARM
    # ---------------------------
    target["ARM"] = (triggers["lt"] - triggers["rt"]) * ARM_SPEED

    # ---------------------------
    # RAMPING (motors only)
    # ---------------------------
    for m in ["LEFT", "RIGHT", "SW", "SE", "NW", "NE"]:
        if abs(target[m]) > abs(out[m]):
            out[m] = ramp_toward(out[m], target[m], RAMP_SPEED)
        else:
            out[m] = target[m]

    # ---------------------------
    # DIRECT OUTPUTS (no ramp)
    # ---------------------------
    out["CAMERA"] = target["CAMERA"]
    out["ARM"] = target["ARM"]

    return out



def remap(x, smin, smax, fmin, fmax):  # takes in a value and the values it ranges between, outputs that value along a different range
    return fmin + ((x - smin) * (fmax - fmin) / (smax - smin))