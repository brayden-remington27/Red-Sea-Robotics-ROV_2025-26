# TODO: (raspi) get webcam camera input and broadcast as an ip camera
# TODO: capture ipcamera input on computer with cv2 in this script
# TODO: use pygame to convert cv2 camera feed to a surface

import pygame
import cv2
from datetime import datetime

cameraCaptures: list = []
cameraDisplays: list = []
stopRecord: bool = False

def init():
    print("Initializing cameras")
    global stopRecord
    
    global cameraCaptures
    global cameraDisplays
    
def quit():
    for i in cameraCaptures:
        i.release()
    cameraCaptures = []
    cv2.destroyAllWindows()
    
    
    
def addCamera(cv2CameraN: int, width: int, height: int):
    print("Adding new camera")
    cameraCaptures.append(cv2.VideoCapture(cv2CameraN))
    cameraDisplays.append(pygame.Surface((width, height)))

# TODO: fix this ai cv2 recording code to work within my program. currently it would halt it, maybe threads or add a writeFrame function to work in the larger loop
def record(cameraN: int):
    cap = cameraCaptures[cameraN]  # get which camera to record.

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30 # Set the desired frames per second

    # Set the name to the timestamp (-milliseconds)
    
    now = datetime.now()
    out = cv2.VideoWriter(f'ROV Code/records/cam({cameraN}){now.year}-{now.month}-{now.day}:{now.hour}.{now.minute}.{now.second}.mp4', 
                          fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Write the flipped frame (optional, just for demonstration)
        out.write(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'): # Press 'q' to quit
            break

    #cap.release()
    out.release()
    cv2.destroyAllWindows()

def CV2FrameAsSurface(cameraN: int, width: int, height: int):  # width & height for scaling
    ret, frame = cameraCaptures[cameraN].read()
    frame = cv2.resize(frame, (width, height))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)
    frame_rgb = cv2.flip(frame_rgb, -1)
    
    return pygame.surfarray.make_surface(frame_rgb)

def asSurface(cameraN: int): # basically a child of CV2FrameAsSurface
    return CV2FrameAsSurface(cameraN, cameraDisplays[cameraN].get_width(), cameraDisplays[cameraN].get_height())

