# TODO: Copy over code from Dylan for Xbox controller
# TODO: Export all inputs as a list of commands, either keyboardInputs or controllerInputs

# Dylan put in about twice as much code to try and deal with the possibilities of multiple controllers (code that wouldn't have worked/mattered),
# I'm not going to do that.

import pygame

values = {}
toggles = {}

XBOXRefrence = {
    "DEADZONE": 0.075,
    
    "BUTTONS": {
        "r_a": 0,
        "r_b": 1,
        "r_x": 2,
        "r_y": 3,
        "ljoy": 9,
        "rjoy": 10,
        #"lt": 6,
        #"rt": 7,
        "lb": 4,
        "rb": 5,
        "back": 6,
        "start": 8
    },

    "AXES": {
        "l_x": 0,
        "l_y": 1,
        "r_x": 3,
        "r_y": 4,
    },

    "HATS":{
        "main": 0
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

def 
