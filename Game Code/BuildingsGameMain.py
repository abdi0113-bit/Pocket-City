import pygame
import random
import time
import math

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
    imageAssets |= DrawGrid.LoadImagesFromFolder('Image Assets/Inventory Sprites/Building Sprite', tileSize/67)
    imageAssets |= DrawGrid.LoadImagesFromFolder('Image Assets/Inventory Sprites/Rarity Background', tileSize/50)
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
    
def StartGame(numPlayers, startingMoney, boardSize):
    players = []

    for i in range(numPlayers):
        players.append(Player.Player(f'Player {i+1}', i + 1, (boardSize)))
        players[i].money += startingMoney

    return players

def PostResizeEvent(screenSize):
    screenWidth, screenHeight = screenSize
    resizeEvent = pygame.event.Event(pygame.VIDEORESIZE, {'size': (screenWidth, screenHeight), 'w': screenWidth, 'h': screenHeight})
    # This adds the event to the built-in Pygame event queue
    pygame.event.post(resizeEvent)

def DoBeforeRound(currentPlayer, gridSize):
    gridWidth, gridHeight = gridSize
    chargeIncrease = 0
    
    # Create blank multiplier and addend tables
    multipliers = [[1 for i in range(gridWidth)] for j in range(gridHeight)]
    coinMultipliers = [[1 for i in range(gridWidth)] for j in range(gridHeight)]
    addends = [[0 for i in range(gridWidth)] for j in range(gridHeight)]

    for row in range(gridHeight):
        for column in range(gridWidth):
            try:
                if currentPlayer.board[row][column]:
                    multipliers, addends, coinMultipliers, chargeIncrease = currentPlayer.board[row][column].beforeRound(currentPlayer, multipliers, addends, coinMultipliers, column, row)
            except:
                [print(i) for i in currentPlayer.board]

    #[print(i) for i in multipliers] # Debug tool
    return multipliers, addends, coinMultipliers, chargeIncrease

# Main funtion
def Main():
    # Clock is set to pygame's clock object
    FPS = 60
    clock = pygame.time.Clock()

    # Screen width and height in pixels
    screenWidth, screenHeight = 640, 480
    # Grid width and height in tiles
    # Start at 3x3
    gridWidth, gridHeight = 3, 3
    gridSizeLimit = 10
    # Tile size in pixelsButton
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

    # Turn & round number starts at 0 to make indexing easier
    currentTurn = 0
    currentRound = 0

    rerollCost = 2
    moneyPerRound = 5
    shopLength = 3

    popups = []

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
        mouseTileX, mouseTileY = mousePos[0] // tileSize, (mousePos[1] - gridOffsetY) // tileSize

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
                        button.x = min(event.w - 60, (gridWidth + 2.5) * tileSize - 60)
                    elif button.name == 'Sell':
                        button.x = min(event.w - 180, (gridWidth + 2.5) * tileSize - 180)
                    elif button.name == 'Reroll':
                        button.x = (gridWidth + 2.25) * tileSize
                        button.y = gridOffsetY + tileSize * 0.25
                    elif button.name == 'Expand':
                        button.x = min(event.w - 230, (gridWidth + 2.5) * tileSize - 230)
                    elif button.name == 'NextRound':
                        button.x = screenWidth - 100
                        button.y = screenHeight - 50

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
                        
                        # If a tile is selected, and a shop item is selected, and the mouse isn't on the shop, and the player can afford the purchase:
                        if selectedTile != (-1, -1) and selectedShopItem > -1 and mouseShopItem == -1 and players[currentTurn].canAfford(players[currentTurn].shop[selectedShopItem].cost) and not currentBoardItem:
                            # Transfer the selected shop item to the current space
                            transferItem = players[currentTurn].shop.pop(selectedShopItem)
                            players[currentTurn].board[selectedTile[1]][selectedTile[0]] = transferItem

                            # Activate when placed ability
                            scoreIncrease, moneyIncrease, players[currentTurn].board = players[currentTurn].board[selectedTile[1]][selectedTile[0]].whenPlaced(players[currentTurn].board, selectedTile[0], selectedTile[1])

                            players[currentTurn].score += scoreIncrease
                            players[currentTurn].money += moneyIncrease
                            
                            players[currentTurn].spendMoney(transferItem.cost)
                            selectedShopItem = -1
                            selectedTile = (-1, -1)
                        else:
                            # If no selected shop item, or current one is too expensive, select current tile
                            pass
                        
                            
                    
                    for button in buttons:
                        if button.isOver(mousePos) and button.shown:
                            #print(button.name)
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
                                players = StartGame(numberOfPlayers, moneyPerRound, (gridWidth, gridHeight))
                                buttons = []
                                buttons.append(UserInterface.Button('NextTurn', (128,128,128), (gridWidth + 2.5) * tileSize - 60, 25, 100, 30, 'Next Turn'))
                                buttons.append(UserInterface.Button('Sell', (128,128,128), (gridWidth + 2.5) * tileSize - 180, 25, 100, 30, 'Sell ($)'))
                                buttons.append(UserInterface.Button('Reroll', (128,128,128), (gridWidth + 2.25) * tileSize, 75, 100, 30, image=imageAssets['Reload Icon']))
                                buttons.append(UserInterface.Button('Expand', (128,128,128), (gridWidth + 2.5) * tileSize - 230, 25, 200, 30, f'Expand Grid (${players[currentTurn].expandCost})'))
                                buttons.append(UserInterface.Button('NextRound', (128,128,128), screenWidth - 100, screenHeight - 50, 100, 30, 'Next Round'))

                            elif button.name == 'PlayerSelector':
                                numberOfPlayers = result

                            elif button.name == 'NextTurn':
                                # Next turn
                                players[currentTurn].money = 0 # Get rid of unspent money

                                # Unselect shop and tile
                                selectedTile = (-1,-1)
                                selectedShopItem = -1

                                currentTurn += 1

                                if currentTurn == numberOfPlayers:
                                    # Not the new round yet, since action phase still needs to happen
                                    currentTurn = 0
                                    
                                    gameState = 'Action'
                                    startTime = time.time()
                                    players[currentTurn].score = 0
                                    selectedTile = (0,0)
                                    activatedYet = False
                                                         
                                gridHeight = len(players[currentTurn].board)
                                gridWidth = len(players[currentTurn].board[0])
                                players[currentTurn].rerollShop(currentRound, shopLength)

                                if gameState == 'Action':
                                    # Do before round
                                    multipliers, addends, coinMultipliers, chargeIncrease = DoBeforeRound(players[currentTurn], (gridWidth, gridHeight))
                                    players[currentTurn].charge += chargeIncrease


                                for button in buttons:
                                    if button.name == 'Expand':
                                        button.updateMessage(players[currentTurn].expandCost)

                                # Post a resize event to the event queue
                                PostResizeEvent((screenWidth, screenHeight))

                            elif button.name == 'Sell':
                                # I need to use oldSelectedTile since, by the time the click registers, selectedTile will already be (-1, -1), unselected
                                players[currentTurn].money += players[currentTurn].board[oldSelectedTile[1]][oldSelectedTile[0]].sellAmt
                                players[currentTurn].board[oldSelectedTile[1]][oldSelectedTile[0]] = None
                            
                            elif button.name == 'Reroll':
                                if not players[currentTurn].money < rerollCost:
                                    selectedShopItem = -1
                                    players[currentTurn].rerollShop(currentRound, shopLength)
                                    players[currentTurn].money -= rerollCost

                            elif button.name == 'Expand':
                                if not players[currentTurn].money < players[currentTurn].expandCost and gridWidth < gridSizeLimit and gridHeight < gridSizeLimit:
                                    gridHeight += 1
                                    gridWidth += 1
                                    [row.append(None) for row in players[currentTurn].board]
                                    players[currentTurn].board.append([None for i in range(gridWidth)])

                                    # Post a resize event to the event queue
                                    PostResizeEvent((screenWidth, screenHeight))

                                    players[currentTurn].money -= players[currentTurn].expandCost

                                    # Increase expand cost
                                    players[currentTurn].expandCost *= 2
                                    if gridHeight == gridSizeLimit or gridWidth == gridSizeLimit:
                                        button.updateMessage('MAX')
                                    else:
                                        button.updateMessage(f'${players[currentTurn].expandCost}')
                            
                            elif button.name == 'NextRound':
                                players.sort(key = lambda p: p.turn) # Sorts players list back into turn order

                                gameState = 'Active'
                                    
                    pressedButtons = []

                    #print(mouseShopItem)
                    if mouseShopItem > -1 and gameState == 'Active':
                        # Select current shop item, if any
                        if mouseShopItem == selectedShopItem:
                            selectedShopItem = -1
                        else:
                            selectedShopItem = mouseShopItem
                
                if event.button == 3: # Right click
                    if mouseShopItem > -1 and gameState == 'Active':
                        players[currentTurn].shop[mouseShopItem].frozen ^=  True
    
        screenSettings = (screenWidth, screenHeight, tileSize, gridOffsetY)
        if gameState == 'Active':
            # Draw a blue background
            pygame.draw.rect(screen, (115, 197, 245), (0,0,(gridWidth + 2.5) * tileSize, max(gridOffsetY + gridHeight * tileSize, ((len(players[currentTurn].shop)) + 0.5) * tileSize + gridOffsetY)), 0)

            DrawGrid.DrawGrid(screen, imageAssets, screenSettings, players[currentTurn].board, (gridWidth, gridHeight))
            DrawGrid.DrawMouse(screen, imageAssets, players[currentTurn].board, selectedTile, screenSettings, (gridWidth, gridHeight))
            UserInterface.DrawHud(screen, imageAssets, screenSettings, (gridWidth, gridHeight), players[currentTurn], gameState)
            mouseShopItem = UserInterface.DrawShop(screen, imageAssets, rarityFiles, screenSettings, (gridWidth, gridHeight), players[currentTurn], selectedShopItem)
        
        if gameState == 'Action':
            pygame.draw.rect(screen, (115, 197, 245), (0,0,(gridWidth + 2.5) * tileSize, max(gridOffsetY + gridHeight * tileSize, ((len(players[currentTurn].shop)) + 0.5) * tileSize + gridOffsetY)), 0)

            DrawGrid.DrawGrid(screen, imageAssets, screenSettings, players[currentTurn].board, (gridWidth, gridHeight))
            DrawGrid.DrawMouse(screen, imageAssets, players[currentTurn].board, selectedTile, screenSettings, (gridWidth, gridHeight))
            UserInterface.DrawHud(screen, imageAssets, screenSettings, (gridWidth, gridHeight), players[currentTurn], gameState)

            # This wait time assumes all tiles are occupied - empty board will take half the time
            waitSeconds = 10
            waitTime = waitSeconds/(gridWidth*gridHeight)

            # Delete popups older than 1 second
            for popupIndex, popup in enumerate(popups):
                if time.time() - popup['Time'] > 1:
                    popups.pop(popupIndex)

            # Show popups
            for popup in popups:
                UserInterface.Popup(screen, tileSize, popup['Score'], popup['Money'], popup['X'], popup['Y'], popup['Opacity'])
                popup['Y'] -= 60 * dt
                popup['Opacity'] -= 128 * dt


            # Activate when the time is halfway up
            if time.time() - startTime > waitTime/2:
                if not activatedYet:
                    scorePopupX = (selectedTile[0] + 0.25) * tileSize
                    scorePopupY = (selectedTile[1] + 0.5) * tileSize + gridOffsetY

                    activatedYet = True
                    # Activate the current tile
                    if players[currentTurn].board[selectedTile[1]][selectedTile[0]]:
                        scoreIncrease, moneyIncrease = players[currentTurn].board[selectedTile[1]][selectedTile[0]].whenActivated(players[currentTurn], selectedTile[0], selectedTile[1], multipliers, addends, coinMultipliers)
                        
                        # Apply bonuses
                        scoreIncrease += addends[selectedTile[1]][selectedTile[0]]
                        scoreIncrease *= multipliers[selectedTile[1]][selectedTile[0]]
                        scoreIncrease *= (players[currentTurn].charge/100) + 1
                        moneyIncrease *= coinMultipliers[selectedTile[1]][selectedTile[0]]

                        # Change score
                        players[currentTurn].score += round(scoreIncrease)
                        players[currentTurn].money += round(moneyIncrease)

                        # Create a popup
                        popups.append({'Time': time.time(),
                                       'Score': round(scoreIncrease), 
                                       'Money': round(moneyIncrease),
                                       'X': scorePopupX,
                                       'Y': scorePopupY,
                                       'Opacity': 255})

                    else:
                        # If tile is empty, skip to the next tile
                        startTime -= waitTime

            # If elapsed time has reached the threshhold
            if time.time() - startTime > waitTime:
                
                x, y = selectedTile
                x += 1

                if x == gridWidth:
                    x = 0
                    y += 1

                    if y == gridHeight:
                        # Last square, next player
                        currentTurn += 1
                        popups = []
                        
                        if currentTurn == numberOfPlayers:                            
                            # End of action phase, next round
                            currentRound += 1
                            currentTurn = 0
                            selectedTile = (-1, -1)

                            # Update shop length and per round
                            if currentRound % 5 == 0:
                                shopLength += 1

                            #print(currentRound, moneyPerRound)
                            if currentRound % 2 == 0:
                                moneyPerRound += 1
                            
                            # Update lives and money
                            for player in players:
                                player.money += moneyPerRound
                            
                            # The lambda function returns the score of the input, and is used as a sorting key
                            # Reverse = True means sort from high to low
                            players.sort(key = lambda p: p.score, reverse=True)
                            
                            # Prints the score of each player
                            #[print(f'{i.name}: {i.score}') for i in players]

                            medianScore = UserInterface.Median(players)
                            for index, player in enumerate(players):
                                if player.score < medianScore:
                                    players[index].lives -= 1

                            gameState = 'Results'

                        else:
                            selectedTile = (0, 0)
                            players[currentTurn].score = 0
                            
                            # Do before round
                            gridHeight = len(players[currentTurn].board)
                            gridWidth = len(players[currentTurn].board[0])

                            multipliers, addends, coinMultipliers, chargeIncrease = DoBeforeRound(players[currentTurn], (gridWidth, gridHeight))
                        
                        gridHeight = len(players[currentTurn].board)
                        gridWidth = len(players[currentTurn].board[0])

                        PostResizeEvent((screenWidth, screenHeight))

                    else:
                        selectedTile = (x, y)
                
                else:
                    selectedTile = (x, y)

                # Reset elapsed time
                startTime = time.time()
                activatedYet = False
        
        if gameState == 'Results':
            # Draw a blue background
            pygame.draw.rect(screen, (115, 197, 245), (0,0,screenWidth, screenHeight), 0)
            UserInterface.DisplayScores(screen, imageAssets, screenSettings, players)

        sellAvailable = (False, None)
        if gameState != 'Action':
            # Don't process buttons during action phase
            if gameState != 'Start' and selectedTile != (-1, -1):
                if players[currentTurn].board[selectedTile[1]][selectedTile[0]]:
                    sellAvailable = (True, players[currentTurn].board[selectedTile[1]][selectedTile[0]])
            # Draw the buttons
            UserInterface.DrawButtons(screen, buttons, gameState, sellAvailable)


        if gameState == 'Active' or gameState == 'Action':
            # Draw the mouseover text
            if mouseShopItem > -1: # If the mouse is on the shop
                UserInterface.MouseoverText(screen, mousePos, players[currentTurn].shop[mouseShopItem].message)

            if not (mouseTileX >= gridWidth or mouseTileY >= gridHeight or mouseTileX < 0 or mouseTileY < 0): # If in bounds
                try:
                    if players[currentTurn].board[mouseTileY][mouseTileX]: # If building exists
                        UserInterface.MouseoverText(screen, mousePos, players[currentTurn].board[mouseTileY][mouseTileX].message)
                except:
                    [print(i) for i in players[currentTurn].board]
        
        
        pygame.display.flip() # This updates the entire screen

    # This makes pygame quit nicely
    pygame.quit()

#This function runs everything. If you want the game to do something, it needs to go in main()
if __name__ == "__main__":

    Main()





