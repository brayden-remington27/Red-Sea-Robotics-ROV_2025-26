# import pigpio
# pi = pigpio.pi('raspberrypi.local')   # or IP address of the Pi
# pi.write(17, 0)
# print(pi.connected)

import pygame
import ast # literally only using for parsing tuples from config
import configparser

import draw
import inputs
import camera
import sterioscope
import sensors



def init(config):
    
    #################   VALUES EXTRACTED FROM SETTINGS FILE   ###############################
    PINS = {
        "FRONT_LEFT_PIN": config.getint("THRUSTERS", "FRONT_LEFT_PIN", fallback=19),
        "FRONT_RIGHT_PIN": config.getint("THRUSTERS", "FRONT_RIGHT_PIN", fallback=16),
        "UP_BACKLEFT_PIN": config.getint("THRUSTERS", "UP_BACKLEFT_PIN", fallback=21),
        "UP_BACKRIGHT_PIN": config.getint("THRUSTERS", "UP_BACKRIGHT_PIN", fallback=20),
        "UP_FRONTLEFT_PIN": config.getint("THRUSTERS", "UP_FRONTLEFT_PIN", fallback=26),
        "UP_FRONTRIGHT_PIN": config.getint("THRUSTERS", "UP_FRONTRIGHT_PIN", fallback=6),

        "ARM_PIN": config.getint("GENERAL", "ARM_PIN", fallback=13),
        "CAMERA_PIN": config.getint("GENERAL", "CAMERA_PIN", fallback=25),
        "LEAK_PIN": config.getint("GENERAL", "LEAK_PIN", fallback=5)
    }

    MAX_PW = config.getfloat("PWM", "MAX_PW", fallback=0.0019)
    MIN_PW = config.getfloat("PWM", "MIN_PW", fallback=0.0011)

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
    
    
    camera.screenInit(CAM1WIDTH, CAM1HEIGHT)
    draw.init(WIDTH, HEIGHT, BACKGROUND_COLOR, resize=False)  # Create the info window










def loop():
    running = True
    while running:  # Start control loop
        
        ###### JOYSTICK TO MOTORS ######
        
        
        
        displayData = {
            "status": sensors.flags,  # Flags of what is connected (cam, gyro, therm) and errors/warnings (leaks, etc)
            "data": sensors.data,  # temp, gyro, accel
            "settings": inputs.toggles,  # PWM settings from controller to motors, different modes of movement, recording stats, controling mode (contr or keyb). buttons on contr
            "joystickValues": inputs.values  # joystick movement percentages/activations (with whatever set limit max % being the furthest the joystick can move, 
            #not just making the joystick cap not change anything after a certain point)
        }
        
        ###### DRAW ######
        # Draw the webcam onto the screen for now, making sure to scale the camera input to the desired size of the surface
        camera.camera1Display = camera.CV2FrameAsSurface(camera.camera1Display.get_width(), camera.camera1Display.get_height())
        
        draw.update(displayData, camera.camera1Display)
        
        if draw.getComputerInputs()[0]:  running = False # Quit if window closed
    draw.quit()
    camera.quit()