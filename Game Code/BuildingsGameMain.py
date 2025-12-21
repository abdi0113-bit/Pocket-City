import pygame
import random

import DrawGrid
import UserInterface

# This initialises pygame
pygame.init()

# This function reloads the images to the correct size
def ReloadImages(screenSize, gridSize):
    tileSize = DrawGrid.calculateTileSize(screenSize, gridSize)
    imageAssets = DrawGrid.LoadImagesFromFolder('Image Assets', tileSize)
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
    gridWidth, gridHeight = 8, 8
    # Tile size in pixels
    tileSize = 50
    # screen variable will store the screen
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
    pygame.display.set_caption("Buildings Game")

    tileSize, imageAssets = ReloadImages((screenWidth, screenHeight), (gridWidth, gridHeight))
    #print(imageAssets)

    backgroundColour = (24,24,48) # Pure black background that everything is drawn on

    selectedTile = (-1,-1) # -1, -1 means unselected

    mapData = [[random.choice(['Brick House Top', '']) for j in range(gridWidth)] for i in range(gridHeight)]

    gameState = 'Active'
    buttons = []
    buttons.append(UserInterface.Button((128,128,128), screenWidth/2, screenHeight/2, 200, 50, 'Start!'))

    # Game loop
    gameIsRunning = True
    while gameIsRunning:
        #Limit FPS - clock.tick() also returns the number of milliseconds since the last call
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000 #This gives a time in seconds
        # dt stands for delta time

        # Clear the screen
        screen.fill(backgroundColour)

        # Run through every event detected by pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # Close window button is pressed
                gameIsRunning = False
            
            if event.type == pygame.VIDEORESIZE: # Screen resize
                # event.h and event.w are methods of the VIDEORESIZE event, which are the new height and width of the window
                # Resize the screen
                screenWidth, screenHeight = event.w, event.h
                screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
            
                # Reload image assets
                tileSize, imageAssets = ReloadImages((screenWidth, screenHeight), (gridWidth, gridHeight))
        
            if event.type == pygame.MOUSEBUTTONDOWN: # On click
                """
                event.button codes:
                1: left click
                2: middle click
                3: right click
                4: scroll up
                5: scroll down
                """
                if event.button == 1 and gameState == 'Active':
                    selectedTile = SelectTile((gridWidth, gridHeight), selectedTile, (event.pos[0] // tileSize, event.pos[1] // tileSize))
    
        screenSettings = (screenWidth, screenHeight, tileSize)
        if gameState == 'Active':
            DrawGrid.DrawGrid(screen, imageAssets, screenSettings, mapData, (gridWidth, gridHeight))
            DrawGrid.DrawMouse(screen, imageAssets, selectedTile, tileSize, (gridWidth, gridHeight))
        elif gameState == 'Start':
            UserInterface.drawButtons(screen, buttons)
        
        pygame.display.flip() # This updates the entire screen

    # This makes pygame quit nicely
    pygame.quit()

#This function runs everything. If you want the game to do something, it needs to go in main()
if __name__ == "__main__":
    Main()