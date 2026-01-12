import pygame
# Supports opacity for fonts, needs to be imported separately
import pygame.ftfont

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

# Button class
class Button():
    def __init__(self, name, colour, x, y, width, height, text='', image=None):
        self.name = name
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.shown = False
        if self.image:
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        fontSize = self.height
        self.font = pygame.font.SysFont('amertype', int(fontSize))

        fontRenderTemp = self.font.render(self.text, True, (0,0,0))
        if fontRenderTemp.get_width() > self.width * 0.9:
            fontSize /= fontRenderTemp.get_width() / (self.width * 0.9)
            self.font = pygame.font.SysFont('amertype', int(fontSize))

    def draw(self, surface, outline = False):
        # This method draws the button on the screen
        textRender = self.font.render(self.text, True, (0,0,0))

        drawWidth = max(self.width, textRender.get_width() * 1.05)
        mousePos = pygame.mouse.get_pos()

        if self.image:
            # Draw the button brighter if it's being hovered over
            currentImage = self.image
            if self.isOver(mousePos):
                currentImage = LightenImage(self.image, 64)

            surface.blit(currentImage, (self.x - self.width/2, self.y - self.height/2))
            
        else:
            if outline:
                pygame.draw.rect(surface, outline, (self.x-4 - drawWidth/2, self.y-4 - self.height/2, drawWidth+8,self.height+8),0)
            
            # Draw the button brighter if it's being hovered over
            if self.isOver(mousePos):
                drawColour = [(colour * 15) // 10 for colour in self.colour]
            else:
                drawColour = self.colour

            pygame.draw.rect(surface, drawColour, (self.x - drawWidth/2, self.y - self.height/2, drawWidth, self.height),0)
        
        if self.text != '':
            surface.blit(textRender, (self.x - textRender.get_width()/2, self.y - textRender.get_height()/2))

    def isOver(self, pos):
        # pos is the mouse position
        text = self.font.render(self.text, True, (0,0,0))
        drawWidth = max(self.width, text.get_width() * 1.05)
        if pos[0] > self.x - drawWidth/2 and pos[0] < self.x + drawWidth/2:
            if pos[1] > self.y - self.height/2 and pos[1] < self.y + self.height/2:
                return True
            
        return False
    
    def click(self): # Returns a value to be used by the main script depending on what the button is
        if self.shown:
            if self.name == 'Start':
                return 'Active'
            elif self.name == 'PlayerSelector':
                newPlayerNum = int(self.text[len(self.text) - 1]) + 1 # This takes the current ending and adds 1
                if newPlayerNum == 5:
                    newPlayerNum = 2
                self.text = f'Players: {newPlayerNum}'
                return newPlayerNum
        
    def resize(self, scaleW, scaleH):
        if self.image:
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        else:
            self.width *= scaleW
            self.height *= scaleH
        
        fontSize = self.height
        self.font = pygame.font.SysFont('amertype', int(fontSize))

        fontRenderTemp = self.font.render(self.text, True, (0,0,0))
        if fontRenderTemp.get_width() > self.width * 0.9:
            fontSize /= fontRenderTemp.get_width() / (self.width * 0.9)
            self.font = pygame.font.SysFont('amertype', int(fontSize))

    def sellAmt(self, currentTile):
        self.text = f'Sell (${currentTile.sellAmt})'
    
    def updateMessage(self, var):
        if self.name == 'Expand':
            self.text = f'Expand Grid (${var})' # In this case var is expand cost


def StampImage(screen, imageAssets, imageToLoad, pos, tileSize, lighten=0):
    try:
        currentImage = imageAssets[imageToLoad]
    except:
        #print(f'ERROR: Failed to load tile {imageToLoad}')
        currentImage = imageAssets['Failed to Load']

    if lighten > 0:
        currentImage = LightenImage(currentImage, lighten)
    
    screen.blit(currentImage, (pos[0] * tileSize, pos[1] * tileSize))


def Median(sortedPlayerList):
    length = len(sortedPlayerList)
    middleIndex = length // 2

    if length % 2 == 0:
        # If the list length is even, average the two middle elements
        medianScore = (sortedPlayerList[middleIndex - 1].score + sortedPlayerList[middleIndex].score) / 2
    else:
        # If the list length is odd, the median is the middle element
        medianScore = sortedPlayerList[middleIndex].score

    return medianScore


def DrawButtons(surface, buttons, gameState, sellAvailable):
    # sellAvailable = (true/false, amount to sell for)
    for button in buttons:
        button.shown = True
        # Some exceptions
        if button.name == 'Sell':
            if sellAvailable[0] and gameState == 'Active':
                button.sellAmt(sellAvailable[1])
            else:
                button.shown = False
            
        elif button.name == 'Expand':
            if sellAvailable[0] or gameState == 'Results':
                button.shown = False

        elif button.name == 'NextTurn' or button.name == 'Reroll':
            if gameState != 'Active':
                button.shown = False
        
        elif button.name == 'NextRound':
            if gameState != 'Results':
                button.shown = False

        # Draw the button
        if button.shown:
            button.draw(surface, (0,0,0))

def DrawHud(surface, imageAssets, screenSettings, gridSize, currentPlayer, gameState):
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]
    gridOffsetY = screenSettings[3]

    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    pygame.draw.rect(surface, (129, 91, 55), (0,0,(gridWidth + 2.5) * tileSize, gridOffsetY), 0)

    # Show player number
    font = pygame.font.SysFont('amertype', 32)
    textRender = font.render(f'Player {currentPlayer.turn}', True, (0,0,0))
    surface.blit(textRender, (5, 17))

    # Show lives
    surface.blit(imageAssets['Lives'], (100, 8))
    textRender = font.render(str(currentPlayer.lives), True, (0,0,0))
    surface.blit(textRender, (145, 17))

    # Show coins
    surface.blit(imageAssets['Coin'], (180, 5))
    textRender = font.render(str(currentPlayer.money), True, (0,0,0))
    surface.blit(textRender, (225, 17))

    # If action phase, show score
    if gameState == 'Action':
        textRender = font.render(f'SCORE: {currentPlayer.score}', True, (0,0,0))
        surface.blit(textRender, (300, 17))


def MouseoverText(screen, mousePos, text):

    font = pygame.font.SysFont('amertype', int(20))
    lines = text.split('\n')

    # This is an inline (lambda) function which draws the rectangle with the specified colour and padding
    drawTextRect = lambda colour, padding:    pygame.draw.rect(screen, colour, (mousePos[0] - (textRender.get_width() + padding)/2, mousePos[1] - textHeight - padding/2, (textRender.get_width() + padding),(textHeight + padding)),0)

    longestLine = font.render(max(lines, key=len), True, (0,0,0))
    textHeight = font.render('|', True, (0,0,0)).get_height() * len(lines)

    textRender = longestLine
    drawTextRect((0,0,0), 12)
    drawTextRect((255,255,255), 8)
    
    for index, line in enumerate(lines):
        textRender = font.render(line, True, (0,0,0))

        screen.blit(textRender, (mousePos[0] - textRender.get_width()/2, mousePos[1] - textHeight + textHeight/len(lines) * (index)))


def DrawShop(surface, imageAssets, rarities, screenSettings, gridSize, currentPlayer, selectedShopItem):
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]
    gridOffsetY = screenSettings[3]

    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    shop = currentPlayer.shop

    mousePos = pygame.mouse.get_pos()

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
        StampImage(surface, imageAssets, item.image, (x-0.4, y+0.1), tileSize, lightness)

        if item.frozen:
            StampImage(surface, imageAssets, "Frozen Background", (x, y), tileSize)

        # Write out the cost and the name
        lines = item.name.split(' ')

        lines.insert(0, f'Cost: {item.cost}') # Insert the cost at the start to print with the name

        fontSize = min((tileSize * 0.8)/(len(lines)), 2 * (tileSize)/len(max(lines, key=len)))
        font = pygame.font.SysFont('amertype', int(fontSize))
        
        for index, line in enumerate(lines):
            # Render the current line of text
            textRender = font.render(line, True, (lightness, lightness, lightness))

            # Calculate vertical position based on line number, font height, and spacing
            surface.blit(textRender, ((x + 1.2) * tileSize, (y + 0.1) * tileSize + index * (font.get_height() * 1.1)))

    return mouseShopItem

def DisplayScores(surface, imageAssets, screenSettings, players):
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]
    gridOffsetY = screenSettings[3]

    medianScore = Median(players)

    for index, player in enumerate(players):
        font = pygame.font.SysFont('amertype', int(48))
        
        # Display name
        textRender = font.render(f'{player.name}:', True, (0,0,0))
        surface.blit(textRender, (20, screenHeight/2 + (index*2 - len(players)) * font.get_height() * 1.5))
        
        # Display lives
        surface.blit(imageAssets['Lives'], (170, screenHeight/2 + (index*2 - len(players)) * font.get_height() * 1.5))
        #Show (-1) if it was just decreased
        if player.score < medianScore:
            textRender = font.render(f'{player.lives} (-1)', True, (0,0,0))
        else:
            textRender = font.render(f'{player.lives}', True, (0,0,0))
        surface.blit(textRender, (210, screenHeight/2 + (index*2 - len(players)) * font.get_height() * 1.5))

        # Display scores
        textRender = font.render(f'Score: {player.score}', True, (0,0,0))
        surface.blit(textRender, (20, screenHeight/2 + (index*2 - len(players) + 1) * font.get_height() * 1.5))

def Popup(surface, tileSize, score, money, x, y, opacity):
    # I use pygame.ftfont here since it supports opacity
    font = pygame.ftfont.SysFont('amertype', tileSize//3)
    scoreColour = (37, 99, 232, int(opacity))
    moneyColour = (232, 220, 37, int(opacity))
    backgroundColour = (0, 0, 0, int(opacity))

    if score != 0:
        if score < 0:
            textRender = font.render(f'{score}', True, scoreColour, backgroundColour)
        else:
            textRender = font.render(f'+{score}', True, scoreColour, backgroundColour)
        
        surface.blit(textRender, (x, y))

    if money != 0:
        if money < 0:
            textRender = font.render(f'-${abs(money)}', True, moneyColour, backgroundColour)
        else:
            textRender = font.render(f'+${money}', True, moneyColour, backgroundColour)
        
        surface.blit(textRender, (x, y + font.get_height() * 1.1))
