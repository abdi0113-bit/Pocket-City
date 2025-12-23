import pygame
import random

import DrawGrid
import UserInterface
import Buildings

# This initialises pygame
pygame.init()

# This function reloads the images to the correct size
def ReloadImages(screenSize, gridSize, shopLength):
    tileSize = DrawGrid.CalculateTileSize(screenSize, gridSize, shopLength)
    imageAssets = DrawGrid.LoadImagesFromFolder('Image Assets', tileSize/50)

    return tileSize, imageAssets


def SelectTile(gridSize, selectedTile, pos):
    if selectedTile == pos: # If the position is the selected tile, unselect it
        return (-1, -1)
    elif pos[0] >= gridSize[0] or pos[1] >= gridSize[1]: # Out of bounds
        return (-1, -1)
    else: # Otherwise just update the selected tile
        return pos

# Main funtion
def Main():
    # Clock is set to pygame's clock object
    FPS = 60
    clock = pygame.time.Clock()

    # Screen width and height in pixels
    screenWidth, screenHeight = 640, 480
    # Grid width and height in tiles
    # Start at 4x4
    gridWidth, gridHeight = 3, 3
    # Tile size in pixels
    tileSize = 50
    # screen variable will store the screen
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
    pygame.display.set_caption("Pocket City")

    shop = []
    # Test the shop
    [shop.append(random.choice(Buildings.commonBuildings)) for i in range(3)]

    gridOffsetY = 50
    #print(imageAssets)

    backgroundColour = (24,24,48) # dark blue background that everything is drawn on

    selectedTile = (-1,-1) # -1, -1 means unselected

    mapData = [['' for j in range(gridWidth)] for i in range(gridHeight)]

    gameState = 'Start'

    buttons = []
    pressedButtons = []
    buttons.append(UserInterface.Button('Start', (128,128,128), screenWidth * 0.5, screenHeight * 0.5, 200, 50, 'Start')) # Start button
    numberOfPlayers = 2
    currentTurn = 1
    buttons.append(UserInterface.Button('PlayerSelector', (128,128,128), screenWidth * 0.5, screenHeight * 0.65, 200, 50, f'Players: {numberOfPlayers}'))

    # Construct a dictionary of rarity background files
    rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
    rarityFiles = dict([(rarity, rarity + ' Rarity Background') for rarity in rarities])

    tileSize, imageAssets = ReloadImages((screenWidth, screenHeight), (gridWidth, gridHeight), len(shop))

    # Game loop
    gameIsRunning = True
    while gameIsRunning:
        #Limit FPS - clock.tick() also returns the number of milliseconds since the last call
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000 #This gives a time in seconds
        # dt stands for delta time

        # Clear the screen
        screen.fill(backgroundColour)

        # Get mouse position
        mousePos = pygame.mouse.get_pos()
        mouseTileX, mouseTileY = mousePos[0] // tileSize, mousePos[1] // tileSize

        # Run through every event detected by pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # Close window button is pressed
                gameIsRunning = False
            
            if event.type == pygame.VIDEORESIZE: # Screen resize
                # event.h and event.w are methods of the VIDEORESIZE event, which are the new height and width of the window

                #Scale the buttons by the amount that the screen changed by
                for button in buttons:
                    if button.name == 'Start':
                        button.x = event.w * 0.5
                        button.y = event.h * 0.5
                    elif button.name == 'PlayerSelector':
                        button.x = event.w * 0.5
                        button.y = event.h * 0.65
                    button.resize(event.w/screenWidth, event.h/screenHeight)
                    
                # Resize the screen
                screenWidth, screenHeight = event.w, event.h
                screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
            
                # Reload image assets
                tileSize, imageAssets = ReloadImages((screenWidth, screenHeight), (gridWidth, gridHeight), len(shop))
                
        
            if event.type == pygame.MOUSEBUTTONDOWN: # On click
                """
                event.button codes:
                1: left click
                2: middle click
                3: right click
                4: scroll up
                5: scroll down
                """
                if event.button == 1:
                    if gameState == 'Active':
                        selectedTile = SelectTile((gridWidth, gridHeight), selectedTile, (event.pos[0] // tileSize, event.pos[1] // tileSize))
                    
                    for button in buttons:
                        if button.isOver(mousePos):
                            pressedButtons.append(button)

            if event.type == pygame.MOUSEBUTTONUP: # On release  
                """
                event.button codes:
                1: left click
                2: middle click
                3: right click
                4: scroll up
                5: scroll down
                """
                if event.button == 1:
                    for button in pressedButtons:
                        if button.isOver(mousePos):
                            result = button.click()

                            if button.name == 'Start':
                                gameState = result
                            elif button.name == 'PlayerSelector':
                                numberOfPlayers = result

                    pressedButtons = []
    
        screenSettings = (screenWidth, screenHeight, tileSize)
        if gameState == 'Active':
            DrawGrid.DrawGrid(screen, imageAssets, screenSettings, mapData, (gridWidth, gridHeight))
            DrawGrid.DrawMouse(screen, imageAssets, selectedTile, tileSize, (gridWidth, gridHeight))
            UserInterface.DrawShop(screen, imageAssets, rarityFiles, shop, screenSettings, (gridWidth, gridHeight))

        elif gameState == 'Start':
            UserInterface.DrawButtons(screen, buttons)
        
        pygame.display.flip() # This updates the entire screen

    # This makes pygame quit nicely
    pygame.quit()

#This function runs everything. If you want the game to do something, it needs to go in main()
if __name__ == "__main__":
    Main()