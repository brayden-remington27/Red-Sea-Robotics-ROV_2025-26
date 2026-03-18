# # import cv2

# # url = "rtsp://10.42.0.187:8554/video0_unicast"
# # cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

# # print("Opened:", cap.isOpened())

# # count = 0
# # while count < 30:
# #     ret, frame = cap.read()
# #     print("ret =", ret, "| shape =", None if frame is None else frame.shape)
# #     if not ret:
# #         break
# #     count += 1

# # cap.release()
# # print("Done")

# import cv2
# #import time
# import pygame

# cap = cv2.VideoCapture('rtsp://10.42.0.187:8554/video0_unicast', cv2.CAP_FFMPEG)
# #start = time.time()
# pygame.init()
# pygame.display.set_caption('test 2')
# window = pygame.display.set_mode((680, 420))


# def CV2FrameAsSurface() -> pygame.Surface:  # width & height for scaling
#     #ret, frame = cap.read()
#     frame = cv2.resize(frame, (680, 420))
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)
#     frame_rgb = cv2.flip(frame_rgb, -1)
    
#     return pygame.surfarray.make_surface(frame_rgb)

# def asSurface(): # basically a child of CV2FrameAsSurface
#     return CV2FrameAsSurface()

# if not cap.isOpened():
    # print("Failed to open RTSP stream")
    # pygame.quit()
    # raise SystemExit

# while True:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     #window.fill((0,0,0))
#     ret, frame = cap.read()
#     if not ret: continue
#     

#     #cv2.imshow('video', frame)

#     window.blit(asSurface(), (0,0))
#     pygame.display.flip()

# cap.release()
# cv2.destroyAllWindows()
# pygame.quit()


import pygame
import subprocess

WIDTH, HEIGHT = 680, 420
URL = "rtsp://10.42.0.187:8554/video0_unicast"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RTSP Viewer")

cmd = [
    "ffmpeg",
    "-rtsp_transport", "tcp",
    "-i", URL,
    "-f", "rawvideo",
    "-pix_fmt", "rgb24",
    "-vf", f"scale={WIDTH}:{HEIGHT}",
    "-"
]

pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)

running = True
frame_size = WIDTH * HEIGHT * 3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    raw = pipe.stdout.read(frame_size)
    if len(raw) != frame_size:
        break

    surface = pygame.image.frombuffer(raw, (WIDTH, HEIGHT), "RGB")
    screen.blit(surface, (0, 0))
    pygame.display.flip()

pipe.terminate()
pygame.quit()