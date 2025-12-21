import pygame

# Button class
class Button():
    def __init__(self, colour, x,y,width,height, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,surface,outline=None):
        # This method draws the button on the screen
        if outline:
            pygame.draw.rect(surface, outline, (self.x-4 - self.width/2, self.y-4 - self.height/2, self.width+8,self.height+8),0)
        
        mousePos = pygame.mouse.get_pos()
        # Draw the button brighter if it's being hovered over
        if self.isOver(mousePos):
            brighter = [(colour * 15) // 10 for colour in self.colour]
            pygame.draw.rect(surface, brighter, (self.x - self.width/2, self.y - self.height/2, self.width, self.height),0)
        else:
            pygame.draw.rect(surface, self.colour, (self.x - self.width/2, self.y - self.height/2, self.width, self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('arial', 60)
            text = font.render(self.text, 1, (0,0,0))
            surface.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

    def isOver(self, pos):
        # pos is the mouse position
        if pos[0] > self.x - self.width/2 and pos[0] < self.x + self.width/2:
            if pos[1] > self.y - self.height/2 and pos[1] < self.y + self.height/2:
                return True
            
        return False
    
def drawButtons(surface, buttons):
    for button in buttons:
        button.draw(surface, (0,0,0))