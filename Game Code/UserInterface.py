import pygame

# Button class
class Button():
    def __init__(self, name, colour, x, y, width, height, text=''):
        self.name = name
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface, outline = False):
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
            font = pygame.font.SysFont('amertype', int(self.height))
            text = font.render(self.text, 1, (0,0,0))
            surface.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

    def isOver(self, pos):
        # pos is the mouse position
        if pos[0] > self.x - self.width/2 and pos[0] < self.x + self.width/2:
            if pos[1] > self.y - self.height/2 and pos[1] < self.y + self.height/2:
                return True
            
        return False
    
    def click(self): # Returns a value to be used by the main script depending on what the button is
        if self.name == 'Start':
            return 'Active'
        elif self.name == 'PlayerSelector':
            newPlayerNum = int(self.text[len(self.text) - 1]) + 1 # This takes the current ending and adds 1
            if newPlayerNum == 5:
                newPlayerNum = 2
            self.text = f'Players: {newPlayerNum}'
            return newPlayerNum
    

def stampImage(screen, imageAssets, imageToLoad, pos, tileSize):
    try:
        currentImage = imageAssets[imageToLoad]
    except:
        print(f'ERROR: Failed to load tile {imageToLoad}')
        currentImage = imageAssets['Failed to Load']
    screen.blit(currentImage, (pos[0] * tileSize, pos[1] * tileSize))


def drawButtons(surface, buttons):
    for button in buttons:
        button.draw(surface, (0,0,0))



def drawShop(surface, imageAssets, rarities, shop, gridSize, tileSize):
    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    itemIndex = 0
    for item in shop:
        stampImage(surface, imageAssets, rarities[item.rarity], (gridWidth + 0.5, itemIndex + 0.5), tileSize)
        stampImage(surface, imageAssets, item.image, (gridWidth + 0.5, itemIndex + 0.5), tileSize)
        itemIndex += 1