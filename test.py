import pygame
import sys

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joysticks found. Connect an Xbox controller and restart the script.")
    sys.exit()
else:
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print(f"Detected controller: {controller.get_name()}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")
        if event.type == pygame.JOYBUTTONUP:
            print(f"Button {event.button} released")

        if event.type == pygame.JOYAXISMOTION:
            print(f"Axis {event.axis} moved to {event.value}")
        
        if event.type == pygame.JOYHATMOTION:
            print(f"Hat {event.hat} moved to {event.value}")

    pygame.time.Clock().tick(60)

pygame.quit()
