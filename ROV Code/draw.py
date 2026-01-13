import pygame

# Start Pygame and create info window
def init(WD, HT, BGC, resize=True):
    print("Initializing Window")
    pygame.init()
    pygame.display.set_caption("ROV Info")
    
    
    global displayValues
    displayValues = []  # List of values for different display aspects (temp, depth, preassure, motor activation, etc)

    ### Global Variables ###
    global window
    global BACKGROUND_COLOR
    global printer
    
    BACKGROUND_COLOR = BGC
    
    window = pygame.display.set_mode((WD, HT), pygame.RESIZABLE if resize else 0)  # Create the window/surface that is drawn to
    printer = TextPrint(45, 36)  # create a printer that writes text to the window surface




# TODO: reformat it so that the camera can be on a seperate window, and so that the warnings are square lights with lables

# Clear and redraw window
def update(data: dict, cameraDisplay: pygame.Surface):
    window.fill(BACKGROUND_COLOR)
    printer.reset()
    
    # Using the text draw class below
    # drawing the status items, brighter if error
    # TODO: implement dynamic changing colors of status text, possibly flashing red highlight for leak detected
    printer.tprint(window, "STATUS:")  # warnings
    printer.indent()
    printer.errprint(window, "ROV Disconnected")
    printer.indent()
    printer.errprint(window, "No Leak Detected", "green")
    printer.errprint(window, "Camera Disconnected")
    printer.errprint(window, "Servo Disconnected")
    printer.errprint(window, "Gyro Disconnected")
    printer.errprint(window, "Thermo Disconnected")
    printer.outdent()
    printer.outdent()
    printer.errprint(window, "Controller Disconnected", "yellow")
    printer.print(window, "")
    
    printer.tprint(window, "DATA:")  # temp/pressure/depth
    printer.print(window, "")
    
    printer.tprint(window, "SETTINGS:")  # Controller settings: movement mode (stabilized, stationary, free, cancel rot), 
    printer.print(window, "")
    
    printer.tprint(window, "CONTROLLER:")  # Controller joystick activations and toggles
    printer.print(window, "")
    
    
    
    # Print Camera Text
    printer.reset()
    printer.x = 755
    printer.tprint(window, "CAMERA:")
    
    # Bring camera1Display from the camera.py to control.py update, and fed to draw.py as cameraDisplay
    window.blit(cameraDisplay, (400, 65))
    
    pygame.display.flip()









######### OTHER FUNCTIONS #########


# Close Pygame
def quit():
    print("Closing Window")
    pygame.quit()
  
# TODO: move to inputs.py script with keyboard inputs (not controller inputs)
# Gets pygame inputs and places booleans into a list
# Primarily used for checking if pygame has quit
def getComputerInputs() -> list:
    inputs = [0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inputs[0] = True
    
    return inputs






'''
This is a small printer helper class to draw text more easily to a pygame surface.

x, y: the current positions for the text, in terms of pixles I think

tprint(): writes a new line to where it's needed with the surface, string, and color 
reset(): resets the position of the text writing to the initial position
indent(): add more to the x pos where the text is being written
unindent(): reduce the x pos where the text is being written
'''

################################################################################
class TextPrint(object):                                                       #
    def __init__(self, tsize=50, size=40):                                     #
        self.size = size                                                       #
        self.tsize = tsize                                                     #
        self.reset()                                                           #
        self.font = pygame.font.Font(None, self.size)                          #
        self.tfont = pygame.font.Font(None, self.tsize)                        #
                                                                               #
    def tprint(self, screen, textString, color="white"):                      #
        textBitmap = self.tfont.render(textString, True, pygame.Color(color))  #
        screen.blit(textBitmap, (self.x, self.y))                              #
        self.y += self.line_height+0.5*self.line_height
        
    def errprint(self, screen, textString, color="orange"):
        textBitmap = self.font.render(textString, True, pygame.Color(color))  #
        screen.blit(textBitmap, (self.x, self.y))                              #
        self.y += self.line_height+0.5*self.line_height
                                                                               #
    def print(self, screen, textString, color="grey"):                         #
        textBitmap = self.font.render(textString, True, pygame.Color(color))   #
        screen.blit(textBitmap, (self.x, self.y))                              #
        self.y += self.line_height                                             #
                                                                               #
    def reset(self):                                                           #
        self.x = 20                                                            #
        self.y = 20                                                            #
        self.line_height = self.size * 3/4                                     #
                                                                               #
    def indent(self):                                                          #
        self.x += 20                                                           #
                                                                               #
    def outdent(self):                                                         #
        self.x -= 20                                                           #
                                                                               #
################################################################################