# TODO: Copy over code from Dylan for Xbox controller
# TODO: Export all inputs as a list of commands, either keyboardInputs or controllerInputs

# Dylan put in about twice as much code to try and deal with the possibilities of multiple controllers (code that wouldn't have worked/mattered),
# I'm not going to do that.

import pygame
pygame.init()
pygame.joystick.init()

inputs: list = [False, False, {
    "thumbsticks": {
        "lx": 0.0,
        "ly": 0.0,
        "rx": 0.0,
        "ry": 0.0
    },
    "hat": (0,0),
    "buttons": {
        "mode": "Stabilized"
    }
}]
toggleMode: bool = True

# primary variable, containing the inputs from the controller, to get data from, and to modify
controller: pygame.joystick.JoystickType = None

def init(usingController: bool=True):
    if usingController:
        
        global controller
        global inputs
        global toggles
        global toggleMode
        
        # Check for and initialize controllers
        if pygame.joystick.get_count() > 0:  # it will only recognize one connected controller
            controller = pygame.joystick.Joystick(0)
            controller.init()
            print("Controller Connected: ", controller.get_name())
            
        else:
            print("No controllers found, defaulting to keyboard input")
            keyboardDefault = True
    elif keyboardDefault:
        # TODO: Implement keyboard controlling code
        pass
            
# As it stands:
# 0: if quit, true
# 1: if return, fullscreen
# 2: controller inputs
def getInputs() -> list:
    for event in pygame.event.get():
        #print("checking inputs")
        if event.type == pygame.QUIT:
            inputs[0] = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                inputs[1] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                inputs[1] = False
        
        if event.type == pygame.JOYAXISMOTION:
            #print("#####################################################################")
            if event.axis == 0:
                inputs[2]["thumbsticks"]["lx"] = event.value
                #print(event.value)
            if event.axis == 1:
                inputs[2]["thumbsticks"]["ly"] = event.value
                #print(event.value)
            if event.axis == 3:
                inputs[2]["thumbsticks"]["rx"] = event.value
                #print(event.value)
            if event.axis == 4:
                inputs[2]["thumbsticks"]["ry"] = event.value
                #print(event.value)
                
            
    
    return inputs

def keyboard_to_controller_activations(keypresses: dict):
    pass
