import pygame
import ast # literally only using for parsing tuples from config
import configparser
import pigpio

import draw
import inputs
import outputs
import camera
import sterioscope
import sensors
import utils

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
    MIN_ACTIVATION = config.getfloat("CONFIG", "MIN_ACTIVATION", fallback=0.10)
    
    WIDTH = config.getint("SCREEN", "WIDTH", fallback=600)
    HEIGHT = config.getint("SCREEN", "HEIGHT", fallback=890)
    # TODO: Add light mode
    BACKGROUND_COLOR = ast.literal_eval(config.get("SCREEN", "BACKGROUND_COLOR", fallback="(31, 31, 31)"))
    
    CAM1WIDTH = config.getint("CAMERA1", "WIDTH", fallback=854)
    CAM1HEIGHT = config.getint("CAMERA1", "HEIGHT", fallback=480)
    
    PI_IP = config.get("NETWORKING", "PI_IP", fallback='raspberrypi.local')

    LEAK = config.getint("GENERAL", "LEAK", fallback=5)

    ########################################################################################
    pi = pigpio.pi(PI_IP)
    print(PI_IP)
    print(pi.connected)
    
    camera.init(PI_IP)
    #camera.addCamera(0, CAM1WIDTH, CAM1HEIGHT)  # main local camera of the computer

    # usbcam/cam, usbcam is main camera, cam is down/backup camera
    camera.addCamera("main", f"rtsp://{PI_IP}:8554/maincam", (1280, 720))  # this is for a rtsp data transfer, change port and stuff if needed
    #camera.addCamera("backup", f"rtsp://{PI_IP}:8554/cam", (1280, 720))
    # TODO: implement more cameras for the arm/main/backup cameras
    
    draw.init(WIDTH, HEIGHT, BACKGROUND_COLOR, resize=False)  # Create the info window
    
    # TODO: Make sure that the ROV, controllers, etc can be disconnected and reconnected while the program is running without crashing it
    outputs.init(config, pi)
    inputs.init(MIN_ACTIVATION, True)
    sensors.init(LEAK, pi)

    utils.init(config)  # TODO: rename this script, its no longer a utils its more of a io bridge or smth






def loop():
    running = True
    while running:  # Start control loop
        
        ## SENSORS ##
        
        sensors.update()  # checks the sensors like leak and temp and set internal vars to it
        
        ###### EXTRACT INPUTS ######
        
        all_inputs = inputs.getInputs()
        ins = all_inputs[2]  # 2: controller inputs
        activations = utils.inToOutPercent(ins["hat"], ins["buttons"], ins["thumbsticks"], ins["triggers"])
        
        
        displayData = {
            "status": sensors.flags,  # Flags of what is connected (cam, gyro, therm) and errors/warnings (leaks, etc)
            "data": sensors.data,  # temp, gyro, accel
            "settings": ins["buttons"], # PWM settings from controller to motors, different modes of movement, recording stats, controling mode (contr or keyb). buttons on contr
            "joystickValues": {
                # TODO: (optional) make the minimum viable activation applicable here to avoid confusion
                "sticks": ins["thumbsticks"],  # joystick movement percentages/activations (with whatever set limit max % being the furthest the joystick can move, not just making the joystick cap not change anything after a certain point)
                "dpad": ins["hat"]
            },
            "motors": activations  # the final activations being sent to the motors, after being processed by control.py
        }
        
        ###### OUTPUTS ######

        #print(activations)
        
        outputs.sendActivations(activations, MAX_PERCENT)
        
        ###### CAMERA ######
        
        
        
        ###### DRAW ######
        
        # FYI: only call getSurface() once per loop to avoid consuming 2 frames in one loop
        camera_surface = pygame.transform.rotate(camera.getSurface("main", (918, 648)), -90)  # if not ins["buttons"][6] else "backup"  #TODO: No longer toggle, add toggle for this case
        draw.update(displayData, camera_surface)
        # print camera status once; details are in draw
        #print(f"camera_surface={camera_surface}")

        if all_inputs[1]:
            print("Toggling Fullscreen")
            pygame.display.toggle_fullscreen()  # Fullscreen if enter is pressed

        ###### FINAL CHECKS ######
        if all_inputs[0]:
            print("Quitting")
            running = False # Quit if window closed
    
    draw.quit()
    camera.quit()
    outputs.quit()