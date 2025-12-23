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
                imageW, imageH = rawImage.get_size()
                scaledImage = pygame.transform.smoothscale(rawImage, (imageW * scale, imageH * scale))
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

def DrawMouse(screen, imageAssets, selectedTile, tileSize, gridSize):
    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    # Get mouse position
    mousePos = pygame.mouse.get_pos()
    mouseTileX, mouseTileY = mousePos[0] // tileSize, mousePos[1] // tileSize

    if mouseTileX < gridWidth and mouseTileY < gridHeight:
        # Stamp mouse overlay
        if selectedTile == (-1, -1): # If unselected
            StampImage(screen, imageAssets, 'Hover Tile', (mouseTileX, mouseTileY), tileSize)

        else: # If selected
            StampImage(screen, imageAssets, 'Selected Tile', selectedTile, tileSize)

def TileExists(tileMap, pos):
    if len(tileMap) > pos[1] and len(tileMap[pos[1]]) > pos[0] and pos[1] >= 0 and pos[0] >= 0: # If the tilemap contains that location
        currentTile = tileMap[pos[1]][pos[0]]
        return 1
    else:
        return 0

# Draws the grid
def DrawGrid(screen, imageAssets, screenSettings, tileMap, gridSize):
    
    # tilemap is a 2d array
    # screenSettings contains the height and width of the screen, as well as tile size
    screenWidth = screenSettings[0]
    screenHeight = screenSettings[1]
    tileSize = screenSettings[2]

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
                StampImage(screen, imageAssets, f'Stone Tile {connections}', (column, row), tileSize)
            else:
                StampImage(screen, imageAssets, f'Stone Tile', (column, row), tileSize)

            if len(tileMap) > row and len(tileMap[row]) > column:
                if not tileMap[row][column] in [0, '']:
                    StampImage(screen, imageAssets, tileMap[row][column], (column, row), tileSize)        


def CalculateTileSize(screenSize, gridSize, shopLength):
    screenWidth = screenSize[0]
    screenHeight = screenSize[1]
    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    tryTileHeight = math.ceil(screenHeight/gridHeight)
    tryTileWidth = math.ceil(screenWidth/(gridWidth + 3)) # The +2.2 gives some space for the inventory on the right
    tryInventory = math.ceil(screenHeight/(shopLength + 1))

    return(min(tryTileHeight, tryTileWidth, tryInventory, 100))