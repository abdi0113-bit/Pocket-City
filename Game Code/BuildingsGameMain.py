import pygame
import random

import DrawGrid
import UserInterface
import Buildings
import Player

# This initialises pygame
pygame.init()

# This function reloads the images to the correct size
def ReloadImages(screenSize, gridSize, shopLength=3):
    tileSize = DrawGrid.CalculateTileSize(screenSize, gridSize, shopLength)
    imageAssets = {}
    # The |= operator merges 2 dictionaries
    imageAssets |= DrawGrid.LoadImagesFromFolder('Image Assets/Inventory Sprites', tileSize/50)
    imageAssets |= DrawGrid.LoadImagesFromFolder('Image Assets/Tile Sprites', tileSize/50)
    imageAssets |= DrawGrid.LoadImagesFromFolder('Image Assets/UI', tileSize/50)
    imageAssets |= DrawGrid.LoadImagesFromFolder('Image Assets/Start Screen', min(screenSize[0]/640, screenSize[1]/480))

    return tileSize, imageAssets


def SelectTile(gridSize, selectedTile, pos):
    if selectedTile == pos: # If the position is the selected tile, unselect it
        return (-1, -1)
    elif pos[0] >= gridSize[0] or pos[1] >= gridSize[1] or pos[0] < 0 or pos[1] < 0: # Out of bounds
        return (-1, -1)
    else: # Otherwise just update the selected tile
        return pos
    
def startGame(numPlayers):
    players = []
    startingBoard = [[None for j in range(3)] for i in range(3)]
    startingBoard[1][1] = Buildings.starterTent
    for i in range(numPlayers):
        players.append(Player.Player(100, f'Player {i+1}', 0, i + 1))
    return players

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

    mouseShopItem, selectedShopItem = -1, -1
    oldSelectedTile, selectedTile = (-1, -1), (-1, -1)

    gridOffsetY = 50
    #print(imageAssets)

    backgroundColour = (115, 197, 245) # sky blue background at the start

    selectedTile = (-1,-1) # -1, -1 means unselected

    gameState = 'Start'

    buttons = []
    pressedButtons = []

    numberOfPlayers = 2
    players = []

    # Turn number starts at 0 to make indexing easier
    currentTurn = 0
    currentRound = 0

    # Construct a dictionary of rarity background files
    rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
    rarityFiles = dict([(rarity, rarity + ' Rarity Background') for rarity in rarities])

    tileSize, imageAssets = ReloadImages((screenWidth, screenHeight, gridOffsetY), (gridWidth, gridHeight), 1)

    buttons.append(UserInterface.Button('Start', (128,128,128), screenWidth * 0.25, screenHeight * 0.55, 200, 50, 'Start', imageAssets['Pocket City Button'])) # Start button
    buttons.append(UserInterface.Button('PlayerSelector', (128,128,128), screenWidth * 0.25, screenHeight * 0.8, 200, 50, f'Players: {numberOfPlayers}', imageAssets['Pocket City Button']))

    # Game loop
    gameIsRunning = True
    while gameIsRunning:
        #Limit FPS - clock.tick() also returns the number of milliseconds since the last call
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000 #This gives a time in seconds
        # dt stands for delta time

        # Clear the screen
        screen.fill(backgroundColour)
        if gameState == 'Start':
            screen.blit(imageAssets['Pocket City Background'], (0,0))
            screen.blit(imageAssets['Pocket City Icon'], (0,0))
            screen.blit(imageAssets['Pocket City Title'], (0,0))

        # Get mouse position
        mousePos = pygame.mouse.get_pos()
        mouseTileX, mouseTileY = mousePos[0] // tileSize, mousePos[1] // tileSize

        # Run through every event detected by pygame
        for event in pygame.event.get():

            if event.type == pygame.QUIT: # Close window button is pressed
                gameIsRunning = False
            
            if event.type == pygame.VIDEORESIZE: # Screen resize
                # event.h and event.w are methods of the VIDEORESIZE event, which are the new height and width of the window

                # Resize the screen
                oldScreenWidth, oldScreenHeight = screenWidth, screenHeight
                screenWidth, screenHeight = event.w, event.h
                screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

                # Reload image assets
                if gameState == 'Start':
                    tileSize, imageAssets = ReloadImages((screenWidth, screenHeight, gridOffsetY), (gridWidth, gridHeight))
                else:
                    tileSize, imageAssets = ReloadImages((screenWidth, screenHeight, gridOffsetY), (gridWidth, gridHeight), len(players[currentTurn].shop))

                #Scale the buttons by the amount that the screen changed by
                for button in buttons:
                    if button.name == 'Start':
                        button.x = event.w * 0.25
                        button.y = event.h * 0.55
                    elif button.name == 'PlayerSelector':
                        button.x = event.w * 0.25
                        button.y = event.h * 0.8
                    elif button.name == 'NextTurn':
                        button.x = min(event.w - 100, (gridWidth + 1.8) * tileSize)
                    elif button.name == 'Sell':
                        button.x = min(event.w - 220, (gridWidth + 0.5) * tileSize)
                    elif button.name == 'Reroll':
                        button.x = min(event.w, (gridWidth + 2.25) * tileSize)
                        button.y = gridOffsetY + tileSize * 0.25

                    # Only some buttons should be resized
                    if button.name in ['Start', 'PlayerSelector']:
                        button.image = imageAssets['Pocket City Button']
                        button.resize(event.w/oldScreenWidth, event.h/oldScreenHeight)
                    if button.name == 'Reroll':
                        button.image = imageAssets['Reload Icon']
                        button.resize(event.w/oldScreenWidth, event.h/oldScreenHeight)
                
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
                        oldSelectedTile = selectedTile

                        selectedTile = SelectTile((gridWidth, gridHeight), selectedTile, (event.pos[0] // tileSize, (event.pos[1] - gridOffsetY) // tileSize))
                        currentBoardItem = players[currentTurn].board[selectedTile[1]][selectedTile[0]]

                        # If a shop item is selected, and the mouse isn't on the shop, and the player can afford the purchase:
                        if selectedShopItem > -1 and mouseShopItem == -1 and players[currentTurn].canAfford(players[currentTurn].shop[selectedShopItem].cost) and currentBoardItem  in [0, '', None]:
                            # Transfer the selected shop item to the current space
                            transferItem = players[currentTurn].shop.pop(selectedShopItem)
                            players[currentTurn].board[selectedTile[1]][selectedTile[0]] = transferItem
                            players[currentTurn].spendMoney(transferItem.cost)
                            selectedShopItem = -1
                            selectedTile = (-1, -1)
                        else:
                            # If no selected shop item, or current one is too expensive, select current tile
                            pass
                        
                            
                    
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
                                backgroundColour = (0, 0, 0)
                                players = startGame(numberOfPlayers)
                                buttons = []
                                buttons.append(UserInterface.Button('NextTurn', (128,128,128), (gridWidth + 1.8) * tileSize, 25, 100, 30, 'Next Turn'))
                                buttons.append(UserInterface.Button('Sell', (128,128,128), (gridWidth + 0.5) * tileSize, 25, 100, 30, 'Sell ($)'))
                                buttons.append(UserInterface.Button('Reroll', (128,128,128), (gridWidth + 2.25) * tileSize, 75, 100, 30, image=imageAssets['Reload Icon']))

                            elif button.name == 'PlayerSelector':
                                numberOfPlayers = result

                            elif button.name == 'NextTurn':
                                currentTurn += 1
                                if currentTurn == numberOfPlayers:
                                    # New round
                                    currentRound += 1
                                    currentTurn = 0
                                    # Unselect shop and tile
                                    selectedTile = (-1,-1)
                                    selectedShopItem = -1
                                    if gameState == 'Action':
                                        gameState = 'Active'
                                    else:
                                        gameState = 'Action'
                                players[currentTurn].rerollShop(currentRound)

                            elif button.name == 'Sell':
                                # I need to use oldSelectedTile since, by the time the click registers, selectedTile will already be (-1, -1), unselected
                                players[currentTurn].money += players[currentTurn].board[oldSelectedTile[1]][oldSelectedTile[0]].sellAmt
                                players[currentTurn].board[oldSelectedTile[1]][oldSelectedTile[0]] = None
                            
                            elif button.name == 'Reroll':
                                if players[currentTurn].money > 0:
                                    players[currentTurn].rerollShop(currentRound)
                                    # Costs $1 to reroll
                                    players[currentTurn].money -= 1

                    pressedButtons = []

                    #print(mouseShopItem)
                    if mouseShopItem > -1 and gameState == 'Active':
                        # Select current shop item, if any
                        if mouseShopItem == selectedShopItem:
                            selectedShopItem = -1
                        else:
                            selectedShopItem = mouseShopItem
    
        screenSettings = (screenWidth, screenHeight, tileSize, gridOffsetY)
        if gameState == 'Active':
            # Draw a blue background
            pygame.draw.rect(screen, (115, 197, 245), (0,0,(gridWidth + 2.5) * tileSize, max(gridOffsetY + gridHeight * tileSize, ((len(players[currentTurn].shop)) + 0.5) * tileSize + gridOffsetY)), 0)

            DrawGrid.DrawGrid(screen, imageAssets, screenSettings, players[currentTurn].board, (gridWidth, gridHeight))
            DrawGrid.DrawMouse(screen, imageAssets, players[currentTurn].board, selectedTile, screenSettings, (gridWidth, gridHeight))
            UserInterface.DrawHud(screen, imageAssets, screenSettings, (gridWidth, gridHeight), players[currentTurn])
            mouseShopItem = UserInterface.DrawShop(screen, imageAssets, rarityFiles, screenSettings, (gridWidth, gridHeight), players[currentTurn], selectedShopItem)
        
        if gameState == 'Action':
            pygame.draw.rect(screen, (115, 197, 245), (0,0,(gridWidth + 2.5) * tileSize, max(gridOffsetY + gridHeight * tileSize, ((len(players[currentTurn].shop)) + 0.5) * tileSize + gridOffsetY)), 0)

            UserInterface.DrawHud(screen, imageAssets, screenSettings, (gridWidth, gridHeight), players[currentTurn])
            DrawGrid.DrawGrid(screen, imageAssets, screenSettings, players[currentTurn].board, (gridWidth, gridHeight))

        sellAvailable = (False, None)
        if gameState == 'Active' or gameState == 'Action':
            if selectedTile != (-1, -1):
                if players[currentTurn].board[selectedTile[1]][selectedTile[0]] not in [0, '', None]:
                    sellAvailable = (True, players[currentTurn].board[selectedTile[1]][selectedTile[0]])
        UserInterface.DrawButtons(screen, buttons, sellAvailable)
        
        pygame.display.flip() # This updates the entire screen

    # This makes pygame quit nicely
    pygame.quit()

#This function runs everything. If you want the game to do something, it needs to go in main()
if __name__ == "__main__":
    Main()