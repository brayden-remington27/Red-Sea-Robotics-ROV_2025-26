# TODO: Copy over code from Dylan for Xbox controller
# TODO: Export all inputs as a list of commands, either keyboardInputs or controllerInputs

# Dylan put in about twice as much code to try and deal with the possibilities of multiple controllers (code that wouldn't have worked/mattered),
# I'm not going to do that.

import pygame

values = {
    "thumbsticks": {
        "lx": 0.0,
        "ly": 0.0,
        "rx": 0.0,
        "ry": 0.0
    },
    "dpad": {
        "UP": 0,
        "RIGHT": 0,
        "LEFT": 0,
        "DOWN": 0,
    },
    "toggles": {
        "mode": "Stabilized"
    }
}

# primary variable, containing the inputs from the controller, to get data from, and to modify
controller: pygame.joystick.JoystickType = None

def init(usingController: bool=True):
    if usingController:
        pygame.joystick.init()
        
        global joystick
        global values
        global toggles
        
        # Check for and initialize controllers
        if pygame.joystick.get_count() > 0:  # it will only recognize one connected controller
            controller = pygame.joystick.Joystick(0)
            controller.init()
            
        else:
            print("No controllers found, defaulting to keyboard input")
            keyboardDefault = True
    elif keyboardDefault:
        # TODO: Implement keyboard controlling code
        pass
            


def get_status():
    pass

def keyboard_to_controller_activations(keypresses: dict):
    pass
