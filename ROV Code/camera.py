# TODO: (raspi) get webcam camera input and broadcast as an ip camera
# TODO: capture ipcamera input on computer with cv2 in this script
# TODO: use pygame to convert cv2 camera feed to a surface

import pygame
import cv2
from datetime import datetime

def screenInit(width, height):
    global camera1Display
    camera1Display = pygame.Surface((width, height))  # this should be more or less the only usage of a display entity here, to make it exist.
    
    # TODO: implement a second camera display for the arm/backup camera
    global camera2Display
    #camera1Display = pygame.Surface((width, height))  # I need different width/heights
    
    
    global cap
    cap = cv2.VideoCapture(0)
    
    
# TODO: fix this ai cv2 recording code to work within my program
def startRecord():
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 30 # Set the desired frames per second

    # Set the name to the timestamp (-milliseconds)
    now = datetime.now()
    out = cv2.VideoWriter(f'ROV Code/records/{now.year}-{now.month}-{now.day}:{now.hour}.{now.minute}.{now.second}.mp4', 
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

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def stopRecord():
    pass


def CV2FrameAsSurface(width, height):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (width, height))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)
    frame_rgb = cv2.flip(frame_rgb, 1)
    
    return pygame.surfarray.make_surface(frame_rgb)

def quit():
    stopRecord()
    cap.release()