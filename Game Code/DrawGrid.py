import pygame
import os
import math

# This function is from Gemini, takes a folder and extracts all the images in itself and its subfolders
def LoadImagesFromFolder(path, tileSize):
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
                scaledImage = pygame.transform.smoothscale(rawImage, (tileSize, tileSize))
                images[name] = scaledImage

    # Returns a dictionary with all the images
    # Keys are filenames, values are the images
    return images

def StampImage(screen, imageAssets, imageToLoad, pos, tileSize):
    try:
        currentTileImage = imageAssets[imageToLoad]
    except:
        currentTileImage = imageAssets['Failed to Load']
    screen.blit(currentTileImage, (pos[0] * tileSize, pos[1] * tileSize))

def DrawMouse(screen, imageAssets, selectedTile, tileSize):
    # Stamp mouse overlay
    if selectedTile == (-1, -1): # If unselected
        # Get mouse position
        mousePos = pygame.mouse.get_pos()
        mouseTileX, mouseTileY = mousePos[0] // tileSize, mousePos[1] // tileSize
        StampImage(screen, imageAssets, 'Hover Tile', (mouseTileX, mouseTileY), tileSize)

    else: # If selected
        StampImage(screen, imageAssets, 'Selected Tile', selectedTile, tileSize)


# Draws the grid
def DrawGrid(screen, imageAssets, screenSettings, tilemap, gridSize):
    
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
            StampImage(screen, imageAssets, 'Stone Tile', (column, row), tileSize)

            if len(tilemap) > row and len(tilemap[row]) > column:
                StampImage(screen, imageAssets, tilemap[row][column], (column, row), tileSize)

def calculateTileSize(screenSize, gridSize):
    screenWidth = screenSize[0]
    screenHeight = screenSize[1]
    gridWidth = gridSize[0]
    gridHeight = gridSize[1]

    tryTileHeight = math.ceil(screenHeight/gridHeight)
    tryTileWidth = math.ceil(screenWidth/gridWidth)

    return(min(tryTileHeight, tryTileWidth))