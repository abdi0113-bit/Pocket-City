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
        self.font = pygame.font.SysFont('amertype', int(self.height))

    def draw(self, surface, outline = False):
        # This method draws the button on the screen
        text = self.font.render(self.text, True, (0,0,0))

        drawWidth = max(self.width, text.get_width() * 1.05)

        if outline:
            pygame.draw.rect(surface, outline, (self.x-4 - drawWidth/2, self.y-4 - self.height/2, drawWidth+8,self.height+8),0)
        
        mousePos = pygame.mouse.get_pos()
        # Draw the button brighter if it's being hovered over
        if self.isOver(mousePos):
            drawColour = [(colour * 15) // 10 for colour in self.colour]
        else:
            drawColour = self.colour

        pygame.draw.rect(surface, drawColour, (self.x - drawWidth/2, self.y - self.height/2, drawWidth, self.height),0)
        
        if self.text != '':
            surface.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

    def isOver(self, pos):
        # pos is the mouse position
        text = self.font.render(self.text, True, (0,0,0))
        drawWidth = max(self.width, text.get_width() * 1.05)
        if pos[0] > self.x - drawWidth/2 and pos[0] < self.x + drawWidth/2:
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
        
    def resize(self, scaleW, scaleH):
        self.width *= scaleW
        self.height *= scaleH
        self.font = pygame.font.SysFont('amertype', int(self.height))


def LightenImage(image, brightnessLevel):
    # Creates a lighter copy of the given image

# Create a copy of the original image to avoid destructive modifications
    lighter_image = image.copy()
    
    # Define the fill color (gray value for even brightening across all channels)
    # A higher value means more brightness added, 0 to 255
    fillColour = (brightnessLevel, brightnessLevel, brightnessLevel)
    
    # Apply the fill color with the BLEND_RGB_ADD flag
    # This adds the fill color values to the pixel values of the image
    lighter_image.fill(fillColour, special_flags=pygame.BLEND_RGB_ADD)
    
    return lighter_image


def StampImage(screen, imageAssets, imageToLoad, pos, tileSize, lighten=0):
    try:
        currentImage = imageAssets[imageToLoad]
    except:
        print(f'ERROR: Failed to load tile {imageToLoad}')
        currentImage = imageAssets['Failed to Load']

    if lighten > 0:
        currentImage = LightenImage(currentImage, lighten)
    
    screen.blit(currentImage, (pos[0] * tileSize, pos[1] * tileSize))


def DrawButtons(surface, buttons):
    for button in buttons:
        button.draw(surface, (0,0,0))


def DrawShop(surface, imageAssets, rarities, shop, screenSettings, gridSize, currentPlayer, selectedShopItem):
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]
    gridOffsetY = screenSettings[3]

    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    mousePos = pygame.mouse.get_pos()

    pygame.draw.rect(surface, (129, 91, 55), (0,0,(gridWidth+2.5)*tileSize,gridOffsetY), 0)

    StampImage(surface, imageAssets, 'Shop Sign', (gridWidth + 0.5, gridOffsetY/tileSize), tileSize)

    mouseShopItem = -1

    for itemIndex, item in enumerate(shop):
        # Stamp the rarity background
        x,y = gridWidth + 0.5, itemIndex + 0.5 + gridOffsetY/tileSize
        imageRect = imageAssets[rarities[item.rarity]].get_rect(topleft = (x*tileSize, y*tileSize))
        
        # Deal with selecting the shop item
        if selectedShopItem == -1:
            if imageRect.collidepoint(mousePos):
                lightness = 64
                mouseShopItem = itemIndex
            else:
                lightness = 0

        else:
            if itemIndex == selectedShopItem:
                lightness = 64
            else:
                lightness = 0
            
            if imageRect.collidepoint(mousePos):
                mouseShopItem = itemIndex

        StampImage(surface, imageAssets, rarities[item.rarity], (x, y), tileSize, lightness)
        # Stamp the building's image
        StampImage(surface, imageAssets, item.image, (x-1, y), tileSize, lightness)

        # Write out the cost and the name
        lines = item.name.split(' ')

        lines.insert(0, f'Cost: {item.cost}') # Insert the cost at the start to print with the name

        fontSize = min((tileSize)/(len(lines)), 2 * (tileSize)/len(max(lines, key=len)))
        font = pygame.font.SysFont('amertype', int(fontSize))
        
        for index, line in enumerate(lines):
            # Render the current line of text
            textRender = font.render(line, True, (lightness, lightness, lightness))

            # Calculate vertical position based on line number, font height, and spacing
            surface.blit(textRender, ((x + 1.1) * tileSize, (y + 0.1) * tileSize + index * (font.get_height() * 1.1)))

    # Show player number
    font = pygame.font.SysFont('amertype', 32)
    textRender = font.render(f'Player {currentPlayer.turn}', True, (0,0,0))
    surface.blit(textRender, (5, 17))


    # Show coins
    surface.blit(imageAssets['Coin'], (100, 5))
    textRender = font.render(str(currentPlayer.money), True, (0,0,0))
    surface.blit(textRender, (145, 17))

    return mouseShopItem

