import pygame

'''
This is a small helper class to draw text more easily to a pygame surface.

x, y: the current positions for the text, in terms of pixles I think

tprint(): writes a new line to where it's needed with the surface, string, and color 
reset(): resets the position of the text writing to the initial position
indent(): add more to the x pos where the text is being written
unindent(): reduce the x pos where the text is being written
'''

################################################################################
class TextPrint(object):                                                       #
    def __init__(self, size):                                                  #
        self.size = size or 40                                                 #
        self.reset()                                                           #
        self.font = pygame.font.Font(None, self.size)                          #
                                                                               #
    def tprint(self, screen, textString, color="white"):                       #
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
    def unindent(self):                                                        #
        self.x -= 20                                                           #
                                                                               #
################################################################################

displayValues = []  # list of values for different

def init(WIDTH, HEIGHT, resize=True):
    pygame.init()
    window = pygame.display.set_mode((600, 890), pygame.RESIZABLE if resize else 0)

def setTemp(temp, immediateUpdate=False):
    pass

def update():
    pygame.display.flip()

def quit():
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((600, 890), pygame.RESIZABLE)
    pygame.display.set_caption("ROV Info")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Exit the loop when the user clicks the close button
        
        window.fill((135, 206, 235))
        
        pygame.display.flip() # Push all updates to the window
    pygame.quit()