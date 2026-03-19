import pygame
import cv2
import subprocess
from datetime import datetime

PI_IP: str

stopRecord: bool = False

cameras: dict = {}

def addCamera(name, source, size: tuple, quiet: bool=True):  # run the pipe opening command (see below) and add to the cameras dictionary. quiet says if the command prints stuff to the console
    w, h = size

    cmd = [
        "ffmpeg",
        # the format (v4l2 or rtsp tcp transport) is put here later 
        "-i", source,
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-vf", f"scale={w}:{h}",
        "-"
    ]
    
    # insert the specifics about the command for each camera
    if source.startswith("/dev/video"):  # can accept video 0, 1, etc
        cmd.insert(1, "-f")
        cmd.insert(2, "v4l2")
    elif source == f"rtsp://{PI_IP}:8554/video0_unicast":  #TODO: generalize for all rtsp's if that's how all the cameras will send
        cmd.insert(1, "-rtsp_transport")
        cmd.insert(2, "tcp")
    
    
    cameras[name] = {
        "source": source,
        "size": size,
        # running the ffmpeg command that gets this "pipe" open
        # stderr printing only if quiet is turned off.
        "pipe": subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL if quiet else subprocess.PIPE, bufsize=10**8)  # start the pipe — the command in the terminal which opens up the receiveing of the broadcast of this camera
        }
    
    print(cameras)  #TODO: coment out if printing
    
    if cameras[name]["pipe"].poll() is not None:
        print(f"Camera {name} failed to start")
    

def getRaw(camera):
    w, h = cameras[camera]["size"]  
    frame_size = w * h * 3  # x3 cuz this is a raw bytemap and its rgb, 3 colors, 3 bytes per pixel
    
    raw = cameras[camera]["pipe"].stdout.read(frame_size)  # get the bytes from the pipe
    
    if len(raw) != frame_size:  # if the stream is interupted, the frame gets shorter, and might mess stuff up down the line. don't send anything if not a full frame
        return None  #TODO: Put this whole thing on threads so if one camera dies the app doesn't
    return raw  # if all is good, send the raw

def getSurface(camera):
    raw = getRaw(camera)
    if raw is not None:
        return pygame.image.frombuffer(raw, (cameras[camera]["size"][0], cameras[camera]["size"][1]), "RGB")
    else:
        return None

def init(piip):
    print("Initializing cameras")
    global stopRecord
    
    global cameraCaptures
    global cameraDisplays
    
    global PI_IP
    PI_IP = piip
    
def quit():
    for name in list(cameras.keys()):
        cameras[name]["pipe"].terminate()
        cameras[name]["pipe"].wait()
        del cameras[name]











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