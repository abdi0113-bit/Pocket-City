import pygame
import random
import math

class Building():
    def __init__(self, name, cost, sellAmt, image, rarity, scoreIncreaseValues, moneyIncreaseValues, message):
        self.name = name
        self.cost = cost
        self.sellAmt = sellAmt
        self.image = image
        self.rarity = rarity
        self.scoreIncreaseActivate = scoreIncreaseValues[0]
        self.scoreIncreasePlace = scoreIncreaseValues[1]
        self.moneyIncreaseActivate = moneyIncreaseValues[0]
        self.moneyIncreasePlace = moneyIncreaseValues[1]
        self.message = message
        self.frozen = False

    
    def multiplyNearby(self, board, multipliers, x, y, amt, size=3, whitelist=[]):
        # Easy function for multiplying the surrounding 8 spaces

        newMultipliers = multipliers
        count = 0

        for row in range(y - (size//2), y + (size//2) + 1):
            for column in range(x - (size//2), x + (size//2) + 1):
                # If not the starting space and not out of bounds
                if (column, row) != (x,y) and not (column < 0 or row < 0 or row >= len(newMultipliers)):
                    if column < len(newMultipliers[row]):
                        # If a tile exists:
                        if board[row][column]:
                            # If the current tile is whitelisted or whitelist is empty 
                            if board[row][column].name in whitelist or whitelist == []:

                                # Multiply the current row/col by the amount
                                newMultipliers[row][column] *= amt
                                # Increment the count
                                count += 1
                                
        return newMultipliers, count
    

    def addToNearby(self, board, addends, x, y, amt, size=3, whitelist=[]):
        # Easy function for adding to the surrounding 8 spaces

        newAddends = addends
        count = 0
        
        for row in range(y - (size//2), y + (size//2) + 1):
            for column in range(x - (size//2), x + (size//2) + 1):
                # If not the starting space and not out of bounds
                if (column, row) != (x,y) and not (column < 0 or row < 0 or row >= len(newAddends)):
                    if column < len(newAddends[row]):
                        # If a tile exists:
                        if board[row][column]:
                            # If the current tile is whitelisted or whitelist is empty 
                            if board[row][column].name in whitelist or whitelist == []:

                                # Add the amount to the row/col
                                newAddends[row][column] += amt
                                # Increment the count
                                count += 1
            
        return newAddends, count


    def findEmptyNearby(self, board, x, y, size=3):
        emptySpots = []

        for row in range(y - (size//2), y + (size//2) + 1):
            for column in range(x - (size//2), x + (size//2) + 1):
                # If not the starting space and not out of bounds
                if (column, row) != (x,y) and not (column < 0 or row < 0 or row >= len(board)):
                    if column < len(board[row]):
                        
                        # If tile is empty:
                        if not board[row][column]:
                            emptySpots.append((column, row))

        return emptySpots
    

    def whenPlaced(self,board,x,y):
        # These are any custom abilities, placeholders for now
        if self.name == 'Farm':
            emptySpaces = self.findEmptyNearby(board,x,y)
            if len(emptySpaces) > 0:
                emptySpace=random.choice(emptySpaces)
                board[emptySpace[1]][emptySpace[0]] = commonBuildings['Crop Field']
        
        elif self.name == 'Condo':
            emptySpaces = self.findEmptyNearby(board,x,y)
            if len(emptySpaces) > 0:
                emptySpace=random.choice(emptySpaces)
                if random.random() < 0.1:
                    # 10% chance of tall house
                    board[emptySpace[1]][emptySpace[0]] = uncommonBuildings['Tall House']
                else:
                    # Otherwise pick a random common house
                    board[emptySpace[1]][emptySpace[0]] = commonBuildings[random.choice(['Log House', 'Brick House', 'Modern House'])]

        elif self.name == 'Fire Station':
            pass
        elif self.name == 'Volcano':
            emptySpaces = self.findEmptyNearby(board,x,y)
            

        elif self.name == 'Giant Statue':
            emptySpaces = self.findEmptyNearby(board,x,y)
            if len(emptySpaces) > 0:
                emptySpace=random.choice(emptySpaces)
                board[emptySpace[1]][emptySpace[0]] = rareBuildings['Church']

        # This will automatically deal with increasing score and money
        return self.scoreIncreasePlace, self.moneyIncreasePlace, board


    def beforeRound(self, currentPlayer, multipliers, addends, x, y):
        newMultipliers, newAddends = multipliers, addends

        chargeIncrease = 0

        # Here go abilities which modify other buildings around them
        if self.name == 'School':
            newAddends, count = self.addToNearby(currentPlayer.board, newAddends, x, y, 10, whitelist=['Brick House', 'Log House', 'Modern House', 'Tall House', 'Condo'])
        
        elif self.name == 'Colloseum':
            # Multiply every common by 5
            for y in range(len(newMultipliers)):
                for x in range(len(newMultipliers)):
                    if currentPlayer.board[y][x] in commonBuildings:
                        newMultipliers[y][x] *= 5

        elif self.name == 'Food Stand':
            newAddends, count = self.addToNearby(currentPlayer.board, newAddends, x, y, 0, whitelist=['Crop Field'])
            # Add 5 to score for every crop field
            newAddends[y][x] += 5 * count

        elif self.name == 'Ferris Wheel':
            newMultipliers, count = self.multiplyNearby(currentPlayer.board, newMultipliers, x, y, 1.5, whitelist=['Food Stand', 'Restaurant', 'Casino', 'Bank'])

        elif self.name == 'Giant Statue':
            newMultipliers, count = self.multiplyNearby(currentPlayer.board, newMultipliers, x, y, 5)

        elif self.name == 'Pool':
            newMultipliers, count = self.multiplyNearby(currentPlayer.board, newMultipliers, x, y, 1, whitelist=['Wind Turbine', 'Power Plant'])
            # Half score for every electrical building
            newMultipliers[y][x] /= 2**count

        elif self.name == 'Mansion':
            newAddends, count = self.addToNearby(currentPlayer.board, newAddends, x, y, 0)
            # Subtract 20 from score for every building
            newAddends[y][x] += -20 * count

        elif self.name == 'Church':
            newMultipliers, count = self.multiplyNearby(currentPlayer.board, newMultipliers, x, y, 1, whitelist=['Church'])
            # Multiply score by 1.5 for every church
            newAddends[y][x] *= 1.1 ** count
            newMultipliers, count = self.multiplyNearby(currentPlayer.board, newMultipliers, x, y, 1, whitelist=['Giant Statue'])
            # Multiply score by 5 for every giant statue
            newAddends[y][x] *= 2.5 ** count

        elif self.name == 'Skyscraper':
            newAddends, count = self.addToNearby(currentPlayer.board, newAddends, x, y, 0, whitelist=['Tall House', 'Condo'])
            # Add 30 to score for every building
            newAddends[y][x] += 30 * count

        elif self.name == 'Castle':
            occupied = []
            # Find all occupied coords and put them in a list
            for row in range(len(currentPlayer.board)):
                    for column in range(len(currentPlayer.board[row])):
                        if currentPlayer.board[row][column]:
                            occupied.append((column, row))
            # Pick 3 random buildings and multiply scores by 2
            random.shuffle(occupied)
            # print(occupied)
            for i in range(3):
                if len(occupied) > 0:
                    chosenBuilding = occupied.pop(0)
                    newMultipliers[chosenBuilding[1]][chosenBuilding[0]] *= 3

        elif self.name == 'Pyramid':
            newMultipliers, count = self.multiplyNearby(currentPlayer.board, newMultipliers, x, y, 3.2, size=5)

        elif self.name == 'Wind Turbine':
            chargeIncrease += 10
        
        elif self.name == 'Power Plant':
            chargeIncrease += 50


        return newMultipliers, newAddends, chargeIncrease


    def whenActivated(self, currentPlayer, x, y, multipliers, addends):
        # These are any custom abilities, placeholders for now
        scoreIncrease, moneyIncrease, newMultiplies = self.scoreIncreaseActivate, self.moneyIncreaseActivate, multipliers
        
        if self.name == 'Resturant':
            pass

        elif self.name == 'Mine Quarry':
            moneyIncrease = random.randint(1,5)

        elif self.name == 'Casino':
            modifierFunc = lambda x: (x - 0.5) / (x - x**2) # This creates the probability distribution
            moneyIncrease = math.ceil(modifierFunc(random.random())) # Apply modifier function
            scoreIncrease = 10 * math.ceil(modifierFunc(random.random())) # Score uses the same function but is multiplied by 10
            
        elif self.name == 'Bridge':
            if x > 0:
                if currentPlayer.board[y][x - 1]:
                    repeatActivationScore, repeatActivationMoney = currentPlayer.board[y][x - 1].whenActivated(currentPlayer, x-1, y, multipliers, addends)
            
                    repeatActivationScore += addends[y][x - 1]
                    repeatActivationScore *= multipliers[y][x - 1]

                    scoreIncrease += repeatActivationScore
                    moneyIncrease += repeatActivationMoney

        elif self.name == 'Airport':
            if x > 0:
                for column in range(0, x):
                    if currentPlayer.board[y][column]:
                        repeatActivationScore, repeatActivationMoney = currentPlayer.board[y][column].whenActivated(currentPlayer, column, y, multipliers, addends)
            
                        repeatActivationScore += addends[y][column]
                        repeatActivationScore *= multipliers[y][column]

                        scoreIncrease += repeatActivationScore
                        moneyIncrease += repeatActivationMoney

        elif self.name == 'Bus Stop':
            if y > 0:
                for row in range(0, y):
                    if currentPlayer.board[row][x]:
                        repeatActivationScore, repeatActivationMoney = currentPlayer.board[row][x].whenActivated(currentPlayer, x, row, multipliers, addends)
            
                        repeatActivationScore += addends[row][x]
                        repeatActivationScore *= multipliers[row][x]

                        scoreIncrease += repeatActivationScore
                        moneyIncrease += repeatActivationMoney

        elif self.name == 'Space Station':
            if x > 0 and y > 0:
                for row in range(0, y):
                    for column in range(0, x):
                        if currentPlayer.board[row][column]:
                            repeatActivationScore, repeatActivationMoney = currentPlayer.board[row][column].whenActivated(currentPlayer, column, row, multipliers, addends)
            
                            repeatActivationScore += addends[row][column]
                            repeatActivationScore *= multipliers[row][column]

                            scoreIncrease += repeatActivationScore
                            moneyIncrease += repeatActivationMoney

        elif self.name == 'Bank':
            moneyIncrease += random.randint(-1,-3)

        
                
                

        # This will automatically deal with increasing score and money
        return scoreIncrease, moneyIncrease


    def whenBought(self, board, multipliers, addends, x, y):
        # UNUSED FOR NOW
        # These are any custom abilities, placeholders for now
        newMultipliers, newAddends, moneyIncrease = multipliers, addends, self.moneyIncreaseActivate

        if self.name == 'Condo':
            pass
        elif self.name == 'Bank':
            moneyIncrease += 6
        elif self.name == 'Giant Statue':
            pass

        return newMultipliers, newAddends
    

    def showMessage(self, surface, pos):
        # Shows the mouseover message when called
        font = pygame.font.SysFont('amertype', 20)
        textRender = font.render(self.message, True, (0, 0, 0))
        surface.blit(textRender, pos)
    

# These lists will store all the data for the buildings

# Example:
Building('Brick House', 5,   3,      'Brick House',   'Common',        (5, 0),              (1, 0),                'This is a\nbasic house')
#             ^         ^    ^             ^             ^              ^  ^                 ^  ^                             ^
#            Name     Cost  Sell      Name of image     Rarity        Score when          Money when                   Mouseover message
#                           cost   file (without .png)           (activated, placed)  (activated, placed)         (use \n for multiple lines)
         

starterTent = Building('Starter Tent', 1, 1,  'Starter Tent', '', (1,0), (0,0), 'Starter Tent\n--------------\n+ 1 Score\nwhen activated.')

commonBuildings =  {'Brick House' : Building('Brick House', 1, 1,  'Brick House', 'Common', (5,0), (0,0), 'Brick House\n--------------\n+ 5 Score\nwhen activated.'),
                    'Log House' : Building('Log House', 1, 1,  'Log House', 'Common', (5,0), (0,0), 'Log House\n--------------\n+ 5 Score\nwhen activated.'),
                    'Modern House' : Building('Modern House', 1, 1, 'Modern House', 'Common', (5,0), (0,0), 'Modern House\n--------------\n+ 5 Score\nwhen activated.'),
                    'Farm' : Building('Farm', 2, 1,  'Barn', 'Common', (10,0), (0,0), 'Farm\n--------------\n+ 10 Score\nwhen activated.\nPlaces a Crop Field\nin an adjacent empty space.'),
                    'Crop Field' : Building('Crop Field', 1, 1,  'Crop Field', 'Common', (0,0), (1,0), 'Crop Field\n--------------\n+ $1\nwhen activated.'),
                    'School' : Building('School', 2, 1, 'School', 'Common', (10,0), (0,0), 'School\n--------------\n+ 10 Score\nwhen activated.\n+ 10 score to\nadjacent House Buildings.'),
                    'Food Stand' : Building('Food Stand', 2, 1,  'Food Stand', 'Common', (5,0), (0,0), 'Food Stand\n--------------\n+ 5 Score\nwhen activated.\n+5 Score for every adjacent\nCrop Field.')}


uncommonBuildings = {'Condo' : Building('Condo', 3, 2,  'Condo', 'Uncommon', (10,0), (0,0), 'Condo\n--------------\n+ 10 Score\nwhen activated.\nPlaces a random\nhouse nearby\nwhen placed.'),
                    'Tall House' : Building('Tall House', 2, 1,  'Tall House', 'Uncommon', (10,0), (0,0), 'Tall House\n--------------\n+ 10 Score\nwhen activated.'),
                    'Pool' : Building('Pool', 3, 2, 'Pool', 'Uncommon', (50,0), (0,0), 'Pool\n--------------\n+ 50 Score\nwhen activated\nIf nearby any electric buildings\nDivide score by 2.'),
                    'Wind Turbine' : Building('Wind Turbine', 2, 1,  'Wind Turbine', 'Uncommon', (10,0), (0,0), 'Wind Turbine\n--------------\n+ 10 Score\nwhen activated.'),
                    'Bridge' : Building('Bridge', 3, 2,  'Bridge', 'Uncommon', (0,0), (0,0), 'Bridge\n--------------\nRepeats the ability\nof the Building\nto the left\nwhen activated.'),
                    'Resturant' : Building('Resturant', 4, 3, 'Resturant', 'Uncommon', (15,0), (0,0), 'Resturant\n--------------\n+ 15 Score\nwhen activated.'),
                    'Mine Quarry' : Building('Mine Quarry', 4, 3, 'Mine Quarry', 'Uncommon', (15,0), (0,0), 'Mine Quarry\n--------------\n+ 15 Score\nand + $1-5\nwhen activated.')}

rareBuildings = {'Power Plant': Building('Power Plant', 5, 4,  'Power Plant', 'Rare', (30,0), (0,0), 'Power Plant\n--------------\n+ 30 Score\nwhen activated.'),
                'Mansion' : Building('Mansion', 5, 4,  'Mansion', 'Rare', (100,0), (0,0), 'Mansion\n--------------\n+ 100 Score\nwhen activated.\n- 20 Score for each\nnearby building.'),
                'Church' : Building('Church', 4, 3, 'Church', 'Rare', (20,0), (0,0), 'Church\n--------------\n+ 20 Score\nwhen activated\nIf church is nearby multiply by 1.1 per church.\nIf giant statue is nearby\nmultiply by 2.5 per statue.'),
                'Hospital' : Building('Hospital', 5, 4, 'Hospital', 'Rare', (20,0), (0,0), 'Hospital\n--------------\n+ 20 Score\nwhen activated.'),
                'Fire Station' : Building('Fire Station', 5, 4, 'Fire Station', 'Rare', (20,0), (0,0), 'Fire Station\n--------------\n+ 20 Score\nwhen activated.'),
                'Ferris Wheel' : Building('Ferris Wheel', 4, 3, 'Ferris Wheel', 'Rare', (15,0), (0,0), 'Ferris Wheel\n--------------\n+ 20 Score\nwhen activated\nMultiplies nearby Business by 1.5.')}

epicBuildings = {'Skyscraper' : Building('Skyscraper', 7, 5,  'Skyscraper', 'Epic', (50,0), (0,0), 'Skyscaper\n--------------\n+ 50 Score\nwhen activated\n+ 30 Score for every\nnearby Tall House or Condo.'),
                'Castle' : Building('Castle', 7, 5, 'Castle', 'Epic', (75,0), (0,0), 'Castle\n--------------\n+ 75 Score\nwhen activated\nTriples score of 3\nrandom buildings on the board.'),
                'Casino' : Building('Casino', 8, 6, 'Casino', 'Epic', (0,0), (0,0), 'Casino\n--------------\nGives random score and money\nwhen activated.'),
                'Bank' : Building('Bank', 6, 4,  'Bank', 'Epic', (30,0), (0,0), 'Bank\n--------------\n+ 30 Score\nand takes away $1 - $3\nwhen activated\n+ $6 when bought.'),
                'Police Station' : Building('Police Station', 6, 5,  'Police Station', 'Epic', (30,0), (0,0), 'Police Station\n--------------\n+ 30 Score\nwhen activated.'),
                'Airport' : Building('Airport', 6, 4,  'Airport', 'Epic', (0,0), (0,0), 'Airport\n--------------\nRepeats all\n Buildings to the left\nwhen activated.'),
                'Bus Stop' : Building('Bus Stop', 6, 4, 'Bus Stop', 'Epic', (0,0), (0,0), 'Bus Stop\n--------------\nRepeats all\nBuildings above\nwhen activated.')}


legendaryBuildings = {'Pyramid' : Building('Pyramid', 9, 7,  'Pyramid', 'Legendary', (500,0), (0,0), 'Pyramid\n--------------\n+ 500 Score\nwhen activated\nMultiplies nearby buildings\nby 3.2 in a 5x5 area.'),
                     'Colloseum' : Building('Colloseum', 8, 6,  'Colloseum', 'Legendary', (400,0), (0,0), 'Colloseum\n--------------\n+ 400 Score\nwhen activated.\nx5 score to all\ncommon buildings.'),
                     'Space Station' : Building('Space Station', 10, 8, 'Space Station', 'Legendary', (200,0), (0,0), 'Space Station\n--------------\n+ 200 Score\nwhen activated\nRepeats all\nBuildings above and to the left.'),
                     'Volcano' : Building('Volcano', 9, 7, 'Volcano', 'Legendary', (1000,0), (0,0), 'Volcano\n--------------\n+ 1000 Score\nwhen activated.'),
                     'Giant Statue' : Building('Giant Statue', 10, 8, 'Giant Statue', 'Legendary', (0,0), (0,0), 'Giant Statue\n--------------\nPlaces a Church nearby\nwhen placed.\nMultiplies nearby buildings\nby 5 when activated.')}

allBuildings = (commonBuildings, uncommonBuildings, rareBuildings, epicBuildings, legendaryBuildings)







