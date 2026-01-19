# import pigpio
# pi = pigpio.pi('raspberrypi.local')   # or IP address of the Pi
# pi.write(17, 0)
# print(pi.connected)

import pygame
import ast # literally only using for parsing tuples from config
import configparser

import draw
import inputs
import outputs
import camera
import sterioscope
import sensors

ins = {}  # a dictionary containing all of the activations from the inputs
motors = {}  # a dictionary containing all of the activations for the motors
camRecording = False  # to see if the cameras are recording

def init(config):
    
    global ins
    global motors
    global camRecording
    
    #################   VALUES EXTRACTED FROM SETTINGS FILE   ###############################
    
    HOST_NAME = config.get("NETWORKING", "HOST_NAME", fallback="192.168.2.1")
    CLIENT_NAME = config.get("NETWORKING", "CLIENT_NAME", fallback="redsearobotics")

    UPDATE_RATE = config.getint("CONFIG", "UPDATE_RATE", fallback=60)
    
    WIDTH = config.getint("SCREEN", "WIDTH", fallback=600)
    HEIGHT = config.getint("SCREEN", "HEIGHT", fallback=890)
    # TODO: Add light mode
    BACKGROUND_COLOR = ast.literal_eval(config.get("SCREEN", "BACKGROUND_COLOR", fallback="(31, 31, 31)"))
    
    CAM1WIDTH = config.getint("CAMERA1", "WIDTH", fallback=854)
    CAM1HEIGHT = config.getint("CAMERA1", "HEIGHT", fallback=480)
    ########################################################################################
    
    
    camera.init()
    camera.addCamera(0, CAM1WIDTH, CAM1HEIGHT)
    # TODO: implement more cameras for the arm/main/backup cameras
    
    draw.init(WIDTH, HEIGHT, BACKGROUND_COLOR, resize=False)  # Create the info window
    outputs.init(config)







def loop():
    running = True
    while running:  # Start control loop
        
        ###### EXTRACT INPUTS ######
        
        ins = inputs.values
        activations = sticks_to_activations(ins)
        
        
        values = inputs.getInputs()[2]  # 2: controller inputs
        displayData = {
            # TODO: replace inputs.values with ins
            "status": sensors.flags,  # Flags of what is connected (cam, gyro, therm) and errors/warnings (leaks, etc)
            "data": sensors.data,  # temp, gyro, accel
            "settings": values["buttons"], # PWM settings from controller to motors, different modes of movement, recording stats, controling mode (contr or keyb). buttons on contr
            "joystickValues": {
                "sticks": values["thumbsticks"],  # joystick movement percentages/activations (with whatever set limit max % being the furthest the joystick can move, not just making the joystick cap not change anything after a certain point)
                "dpad": values["hat"]
            }
        }
        
        ###### OUTPUTS ######
        
        outputs.updateActivations(activations)
        
        ###### CAMERA ######
        
        
        
        ###### DRAW ######
        
        # Draw the WEBCAM onto the screen for now, making sure to scale the camera input to the desired size of the surface
        
        #camera.camera1Display = camera.CV2FrameAsSurface(camera.camera1Display.get_width(), camera.camera1Display.get_height())
        #already in camera.asSurface(1)
        draw.update(displayData, camera.asSurface(0))  # Redraw all the text and data
        if inputs.getInputs()[1]: pygame.display.toggle_fullscreen()  # Fullscreen if enter is pressed
        
        
        
        ###### FINAL CHECKS ######
        if inputs.getInputs()[0]: print("Quitting"); running = False # Quit if window closed
    
    draw.quit()
    camera.quit()

def sticks_to_activations(axes: dict):
    pass