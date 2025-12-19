import pygame

#from [file name] import [func1], [func2], etc

# This initialises pygame
pygame.init()

def main():
    # Declare screen, width, and height to be global
    global screen, screenWidth, screenHeight, clock

    
    #Clock is set to pygame's clock object
    FPS = 60
    clock = pygame.time.Clock()

    # Set up the window parameters
    screenWidth, screenHeight = 640, 480
    # screen variable will store the screen
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
    pygame.display.set_caption("Buildings Game")

    backgroundColour = (0,0,0) # Pure black background that everything is drawn on

    x,y = 0, screenHeight/2

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
                # event.h and event.w are methods of the VIDEORESIZE event
                screenWidth, screenHeight = event.w, event.h
                screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
        
        y = screenHeight/2
        x += 10 * dt
        pygame.draw.circle(screen, (255,255,255), (x, y), 10)
        pygame.draw.circle(screen, (255,255,255), (x+50, y), 10)
        pygame.draw.rect(screen, (255,255,255), (x, y+50, 50,5))

        pygame.display.flip() # This updates the entire screen
    
    # This makes pygame quit nicely
    pygame.quit()

#This function runs everything. If you want the game to do something, it needs to go in main()
if __name__ == "__main__":
    main()
