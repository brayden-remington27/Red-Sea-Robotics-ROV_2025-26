import pygame
import subprocess
import threading

PI_IP: str
cameras = {}


def init(piip):  # generally kinda useless but might as well
    print("Initializing cameras")
    global cameras
    global quitting


    global PI_IP
    PI_IP = piip



def addCamera(name, source, size):
    w, h = size

    cmd = [
        "ffmpeg",
        "-loglevel", "error",
        "-nostats",
        "-i", source,
        "-an",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-vf", f"scale={w}:{h}",
        "pipe:1"  # makes it so that every camera has their own pipe, not all to "-", stdout. they all have their own stout pipe
    ]


    # camera specific additions to the command
    if source.startswith("/dev/video"):
        cmd.insert(1, "-f")
        cmd.insert(2, "v4l2")
    elif source.startswith("rtsp://"):
        cmd.insert(1, "-rtsp_transport")
        cmd.insert(2, "tcp")
        cmd.insert(3, "-fflags")
        cmd.insert(4, "nobuffer")
        cmd.insert(5, "-flags")
        cmd.insert(6, "low_delay")

    # creates the pipe (terminal window basically) with its own stdout, stdin and stderr running the generated command for the input camera
    pipe = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=10**8
    )

    

    # adds all this new data to the cameras dictionary for future refrence
    cameras[name] = {
        "source": source,
        "size": size,
        "pipe": pipe,
        "thread": None,
        "latest": None,  # thread per camera adds to here for rest of program to see/use
        "running": True
    }

    # runs each camera on its own thread to minimize interruptions to the overall program caused by things like dropped frames
    t = threading.Thread(target=_cameraReader, args=(name,), daemon=True)  # runs the cameraReader function with the input arg "name" as a background process (daemon)
    t.start()
    cameras[name]["thread"] = t  # I need to add this in after the dictionary is added to in the first place because the thread requires the dictionary, thus needs to start after it's made

    

def _cameraReader(name):
    cam = cameras[name]  # update from the thread to here
    w, h = cam["size"]
    frame_size = w * h * 3  # 3 bytes per pixel cuz rgb, 3 colors, 3 values

    while cam["running"]:

        raw = cam["pipe"].stdout.read(frame_size)  # get the latest outputs from the pipe

        if len(raw) != frame_size:  # check that the frame is full to remove partial or composited frames
            continue  # if so, run again, don't update

        cam["latest"] = raw  # update the frame with the new data
    
    print("Quitting Camera", name, "\'s thread")


def getSurface(name, scaledDimensions: tuple = None):
    cam = cameras[name]
    raw = cam["latest"]  # pull data from the camera, updated via the individual threads

    if raw is None:  #TODO: check if this is going to freeze all if true
        return None

    w, h = cam["size"]
    scaledDimensions = (w, h) if scaledDimensions == None else scaledDimensions  # this is so inneficient istg #TODO: make this better please i beg you
    def_size = pygame.image.frombuffer(raw, (w, h), "RGB")  # a pygame surface made from the raw data at defaut size
    return pygame.transform.scale(def_size, scaledDimensions)


def quit():
    for name in list(cameras.keys()):  # delete and terminate a bunch of data from the cameras dictionary
        cam = cameras[name]

        cam["running"] = False  # end the loop in the thread's parent function

        if cam["pipe"].poll() is None:  # if it's still running
            cam["pipe"].terminate()  # kill it
        if cam["pipe"].stdout:  # if the stdout of the pipe still eists
            cam["pipe"].stdout.close()  # close it
        
        if cam["thread"] and cam["thread"].is_alive():  # if the thread exists and is open
            cam["thread"].join()  # join the thread back to the main thread
        
        # make sure the ffmpeg is gone
        try:
            cam["pipe"].wait(timeout=1) # wait a second for the timeout
        except subprocess.TimeoutExpired:
            cam["pipe"].kill()  # forcefully get it gone
            cam["pipe"].wait()
        
        del cameras[name]  # get rid of that camera dictionary entry in cameras










# # TODO: fix this ai cv2 recording code to work within my program. currently it would halt it, maybe threads or add a writeFrame function to work in the larger loop
# def record(cameraN: int):
#     cap = cameraCaptures[cameraN]  # get which camera to record.

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')

#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = 30 # Set the desired frames per second

#     # Set the name to the timestamp (-milliseconds)
    
#     now = datetime.now()
#     out = cv2.VideoWriter(f'ROV Code/records/cam({cameraN}){now.year}-{now.month}-{now.day}:{now.hour}.{now.minute}.{now.second}.mp4', 
#                           fourcc, fps, (frame_width, frame_height))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             print("Can't receive frame (stream end?). Exiting ...")
#             break

#         # Write the flipped frame (optional, just for demonstration)
#         out.write(frame)

#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) == ord('q'): # Press 'q' to quit
#             break

#     #cap.release()
#     out.release()
#     cv2.destroyAllWindows()