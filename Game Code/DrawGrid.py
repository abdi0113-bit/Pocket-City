import pygame
import os
import math

# This function is from Gemini, takes a folder and extracts all the images in itself and its subfolders
def LoadImagesFromFolder(path, scale):
    # Empty images dictionary
    images = {}
    """
    os.walk recursively travels a file tree and returns a list of 3-tuples. Each tuple contains:
        1. the filepath of each folder
        2. names of all subfolders contained within the folder
        3. the names of all non-directory files in the folder
    """
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # Any files with .png or .jpg are added
            if filename.endswith('.png') or filename.endswith('.jpg'):
                imgPath = os.path.join(dirpath, filename)
                # Stores the image surface using the filename (without extension) as the key
                name = os.path.splitext(filename)[0]
                # .convert_alpha converts it to the right format, alpha means it works with images that have transparency
                rawImage = pygame.image.load(imgPath).convert_alpha()
                # Get width
                imageW, imageH = rawImage.get_size()
                # Certain images have a hardcoded size
                hardCodedScale = scale
                if name == 'Coin':
                    hardCodedScale = 2
                
                scaledImage = pygame.transform.smoothscale(rawImage, (imageW * hardCodedScale, imageH * hardCodedScale))
                images[name] = scaledImage

    # Returns a dictionary with all the images
    # Keys are filenames, values are the images
    return images

def StampImage(screen, imageAssets, imageToLoad, pos, tileSize):
    try:
        currentTileImage = imageAssets[imageToLoad]
    except:
        print(f'ERROR: Failed to load tile {imageToLoad}')
        currentTileImage = imageAssets['Failed to Load']
    screen.blit(currentTileImage, (pos[0] * tileSize, pos[1] * tileSize))

def MouseoverText(screen, mousePos, tilemap, tileSize, gridOffsetY):
    mouseTileX, mouseTileY = mousePos[0] // tileSize, (mousePos[1] - gridOffsetY) // tileSize

    # Draw the mouseover text
    if tilemap[mouseTileY][mouseTileX]:
        font = pygame.font.SysFont('amertype', int(20))
        
        lines = tilemap[mouseTileY][mouseTileX].message.split('\n')

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


def DrawMouse(screen, imageAssets, tilemap, selectedTile, screenSettings, gridSize):
    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]
    gridOffsetY = screenSettings[3]

    # Get mouse position
    mousePos = pygame.mouse.get_pos()
    mouseTileX, mouseTileY = mousePos[0] // tileSize, (mousePos[1] - gridOffsetY) // tileSize
    
    #print(selectedTile[0], selectedTile[1])
    # Stamp mouse overlay
    if selectedTile == (-1, -1): # If unselected
        if not (mouseTileX >= gridWidth or mouseTileY >= gridHeight or mouseTileX < 0 or mouseTileY < 0):
            StampImage(screen, imageAssets, 'Hover Tile', (mouseTileX, mouseTileY + gridOffsetY/tileSize), tileSize)
            
            # Draw the mouseover text
            MouseoverText(screen, mousePos, tilemap, tileSize, gridOffsetY)

    else: # If selected
        StampImage(screen, imageAssets, 'Selected Tile', (selectedTile[0], selectedTile[1] + gridOffsetY/tileSize), tileSize)

def TileExists(tileMap, pos):
    if len(tileMap) <= pos[1] or len(tileMap[pos[1]]) <= pos[0] or pos[1] < 0 or pos[0] < 0: # If the tile is out of bounds
        return 0
    else:
        #Use this once Vishwa makes the 1 connection
        #currentTile = tileMap[pos[1]][pos[0]]
        #return int(currentTile not in [0, '', None])
        return 1

# Draws the grid
def DrawGrid(screen, imageAssets, screenSettings, tileMap, gridSize):
    
    # tilemap is a 2d array
    # screenSettings contains the height and width of the screen, as well as tile size
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]
    gridOffsetY = screenSettings[3]

    gridWidth = gridSize[0]
    gridHeight = gridSize[1]
    
    for row in range(gridHeight):
        for column in range(gridWidth):
            # Stamp the stone tile
            connections = ''
            connections += str(TileExists(tileMap, (column, row - 1))) # Tile above
            connections += str(TileExists(tileMap, (column + 1, row))) # Tile to right
            connections += str(TileExists(tileMap, (column, row + 1))) # Tile below
            connections += str(TileExists(tileMap, (column - 1, row))) # Tile to left

            #print(f'Stone Tile {connections}')
            if f'Stone Tile {connections}' in imageAssets:
                StampImage(screen, imageAssets, f'Stone Tile {connections}', (column, row + gridOffsetY/tileSize), tileSize)
            else:
                StampImage(screen, imageAssets, f'Stone Tile', (column, row + gridOffsetY/tileSize), tileSize)

            if len(tileMap) > row and len(tileMap[row]) > column:
                if not tileMap[row][column] in [0, '', None]:
                    StampImage(screen, imageAssets, tileMap[row][column].image + ' Top', (column, row + gridOffsetY/tileSize), tileSize)        


def CalculateTileSize(screenSettings, gridSize, shopLength):
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    gridOffsetY = screenSettings[2]

    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    tryTileHeight = math.ceil(screenHeight/gridHeight)
    tryTileWidth = math.ceil(screenWidth/(gridWidth + 3)) # The +3 gives some space for the inventory on the right
    tryInventory = math.ceil(screenHeight/(shopLength + 1) + gridOffsetY/50)

    return(min(tryTileHeight, tryTileWidth, tryInventory, 100))