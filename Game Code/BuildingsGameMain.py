import pygame

import DrawGrid

#from [file2] import [func1], [func2], etc

#etc

# This initialises pygame
pygame.init()

# This function reloads the images to the correct size
def reloadImages(screenSize, gridSize):
    tileSize = DrawGrid.calculateTileSize(screenSize, gridSize)
    imageAssets = DrawGrid.LoadImagesFromFolder('Image Assets', tileSize)
    return tileSize, imageAssets

# Main funtion
def main():
    # Clock is set to pygame's clock object
    FPS = 60
    clock = pygame.time.Clock()

    # Screen width and height in pixels
    screenWidth, screenHeight = 640, 480
    # Grid width and height in tiles
    gridWidth, gridHeight = 10, 10
    # Tile size in pixels
    tileSize = 50
    # screen variable will store the screen
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
    pygame.display.set_caption("Buildings Game")

    tileSize, imageAssets = reloadImages((screenWidth, screenHeight), (gridWidth, gridHeight))

    backgroundColour = (0,0,0) # Pure black background that everything is drawn on

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
                tileSize, imageAssets = reloadImages((screenWidth, screenHeight), (gridWidth, gridHeight))
        
        screenSettings = (screenWidth, screenHeight, tileSize)
        DrawGrid.DrawGrid(screen, imageAssets, screenSettings, [], (gridWidth, gridHeight))

        pygame.display.flip() # This updates the entire screen
    
    # This makes pygame quit nicely
    pygame.quit()

#This function runs everything. If you want the game to do something, it needs to go in main()
if __name__ == "__main__":
    main()