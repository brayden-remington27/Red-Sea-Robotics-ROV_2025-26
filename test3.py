import pygame

pygame.init()
pygame.joystick.init()

controller: pygame.joystick.JoystickType = None


# Check for and initialize controllers
if pygame.joystick.get_count() > 0:  # it will only recognize one connected controller
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print("Controller Connected: ", controller.get_name())
            
else:
    print("No controllers found, defaulting to keyboard input")
    keyboardDefault = True

running = True
while running:
    for event in pygame.event.get():
        #print("checking inputs")
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            print(f"Axis {event.axis} value: {event.value:.3f}")
        elif event.type == pygame.JOYBUTTONDOWN:
            print(f"Button {event.button} pressed")
        elif event.type == pygame.JOYBUTTONUP:
            print(f"Button {event.button} released")
        elif event.type == pygame.JOYHATMOTION:
            print(f"Hat {event.hat} value: {event.value}")
        
pygame.quit()