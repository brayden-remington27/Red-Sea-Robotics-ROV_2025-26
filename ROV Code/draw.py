import pygame
import math  # for rounding

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
    printer = TextPrint(45, 30)  # create a printer that writes text to the window surface




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
    printer.errprint(window, "ROV Disconnected", "grey" if data["status"]["piConnect"] else "orange")
    printer.indent()
    printer.errprint(window, "No Leak Detected", "green")
    printer.errprint(window, "Camera Disconnected")
    printer.errprint(window, "Servo Disconnected")
    printer.errprint(window, "Gyro Disconnected")
    printer.errprint(window, "Thermo Disconnected")
    printer.outdent()
    printer.errprint(window, "Controller Disconnected", "yellow")
    printer.outdent()
    printer.print(window, "")
    printer.print(window, "")
    
    printer.tprint(window, "DATA:")  # temp/pressure/depth. mostlly gotten from control.py's displayData
    printer.indent()
    printer.print(window, f"Temp (in): {data["data"]["intTemp"]}")
    printer.print(window, f"Temp (ex): {data["data"]["extTemp"]}")
    printer.print(window, f"Pressure: {data["data"]["pressure"]}")
    printer.print(window, f"Depth: {data["data"]["depth"]}")
    printer.outdent()
    printer.print(window, "")
    printer.print(window, "")
    
    printer.tprint(window, "SETTINGS:")  # Controller settings: movement mode (stabilized, stationary, free, cancel rot), 
    printer.indent()
    printer.print(window, f"Movement Activaion Modifier: {data["settings"]["mode"]}")  # data["settings"] is the same as displayData["settings"], which gets data from input.values["toggles"]
    printer.outdent()
    printer.print(window, "")
    printer.print(window, "")
    
    printer.tprint(window, "CONTROLLER | MOTORS")  # Controller joystick activations and toggles
    #print(round(data["joystickValues"]["sticks"]["lx"], 2))
    printer.print(window, f" LX: {round(data["joystickValues"]["sticks"]["lx"], 2): .2f}  | R:  {0.0}")  # round the display values to 2 decimal points
    printer.print(window, f" LY: {round(data["joystickValues"]["sticks"]["ly"], 2): .2f}  | L:  {0.0}")  # with the ": .2f", it turns the - to a space with the " ", and ensures 2 decimal points with ".2f"
    printer.print(window, f" RX: {round(data["joystickValues"]["sticks"]["rx"], 2): .2f}  | NW: {0.0}")
    printer.print(window, f" RY: {round(data["joystickValues"]["sticks"]["ry"], 2): .2f}  | NE: {0.0}")
    printer.print(window, f"            | SW: {0.0}")
    printer.print(window, f"            | SE: {0.0}")
    printer.outdent()
    printer.print(window, "")
    printer.print(window, "")
    
    
    
    # Print Camera Text
    printer.reset()
    printer.x = 875
    printer.tprint(window, "CAMERA:")
    
    # Bring camera1Display from the camera.py to control.py update, and fed to draw.py as cameraDisplay
    window.blit(cameraDisplay, (500, 65))
    
    pygame.display.flip()









######### OTHER FUNCTIONS #########


# Close Pygame
def quit():
    print("Closing Window")
    pygame.quit()
  
# TODO: move to inputs.py script with keyboard inputs (not controller inputs)
# Gets pygame inputs and places booleans into a list
# Primarily used for checking if pygame has quit




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
        self.font = pygame.font.Font("ROV Code/textures/Space Mono/SpaceMono-Bold.ttf", self.size)
        self.tfont = pygame.font.Font(None, self.tsize)                        #
                                                                               #
    def tprint(self, screen, textString, color="white"):                       #
        textBitmap = self.tfont.render(textString, True, pygame.Color(color))  #
        screen.blit(textBitmap, (self.x, self.y))                              #
        self.y += self.title_height
        
    def errprint(self, screen, textString, color="orange"):
        textBitmap = self.font.render(textString, True, pygame.Color(color))   #
        screen.blit(textBitmap, (self.x, self.y))                              #
        self.y += self.line_height
                                                                               #
    def print(self, screen, textString, color="grey"):                         #
        textBitmap = self.font.render(textString, True, pygame.Color(color))   #
        screen.blit(textBitmap, (self.x, self.y))                              #
        self.y += self.line_height                                             #
                                                                               #
    def reset(self):                                                           #
        self.x = 20                                                            #
        self.y = 20
        self.title_height = self.size*1.2                                      #
        self.line_height = self.size                                           #
                                                                               #
    def indent(self):                                                          #
        self.x += 20                                                           #
                                                                               #
    def outdent(self):                                                         #
        self.x -= 20                                                           #
                                                                               #
################################################################################