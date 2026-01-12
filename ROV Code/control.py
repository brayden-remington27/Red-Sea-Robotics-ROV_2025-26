# import pigpio
# pi = pigpio.pi('raspberrypi.local')   # or IP address of the Pi
# pi.write(17, 0)
# print(pi.connected)

import pygame

import draw
import inputs
import camera
import sterioscope
import sensors



def init(config):
    draw.init()

def loop():
    running = True
    while running:  # Start control loop
        