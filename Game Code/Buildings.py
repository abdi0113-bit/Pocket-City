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

    def whenActivated(self):
        # These are any custom abilities, placeholders for now
        scoreIncrease, moneyIncrease = self.scoreIncreaseActivate, self.moneyIncreaseActivate
        
        if self.name == 'Resturant':
            pass

        elif self.name == 'Mine Quarry':
            moneyIncrease = random.randint(1,5)

        elif self.name == 'Casino':
            modifierFunc = lambda x: (x - 0.5) / (x - x**2) # This creates the probability distribution
            moneyIncrease = math.ceil(modifierFunc(random.random())) # Apply modifier function
            scoreIncrease = 10 * math.ceil(modifierFunc(random.random())) # Score uses the same function but is multiplied by 10
            
            #print(moneyIncrease, scoreIncrease) # Debug tool

        # This will automatically deal with increasing score and money
        return scoreIncrease, moneyIncrease

    def whenPlaced(self):
        # These are any custom abilities, placeholders for now
        if self.name == 'Barn':
            pass
        elif self.name == 'Fire Station':
            pass
        elif self.name == 'Volcano':
            pass
        elif self.name == 'Giant Statue':
            pass

        # This will automatically deal with increasing score and money
        return self.scoreIncreasePlace, self.moneyIncreasePlace

    def multiply3x3(self, board, multipliers, x, y, amt, whitelist=[]):
        # Easy function for multiplying the surrounding 8 spaces

        newMultipliers = multipliers
        count = 0

        for row in [y-1, y, y+1]:
            for column in [x-1, x, x+1]:
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
    
    def addTo3x3(self, board, addends, x, y, amt, whitelist=[]):
        # Easy function for adding to the surrounding 8 spaces

        newAddends = addends
        count = 0
        
        for row in [y-1, y, y+1]:
            for column in [x-1, x, x+1]:
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

    def beforeRound(self, board, multipliers, addends, x, y):
        newMultipliers, newAddends = multipliers, addends

        # Here go abilities which modify other buildings around them
        if self.name == 'School':
            newMultipliers, count = self.multiply3x3(board, newMultipliers, x, y, 2, whitelist=['Brick House', 'Log House', 'Modern House', 'Tall House', 'Condo'])

        return newMultipliers, newAddends

    def whenBought(self):
        # UNUSED FOR NOW
        # These are any custom abilities, placeholders for now
        if self.name == 'Food Stand':
            pass
        elif self.name == 'Condo':
            pass
        elif self.name == 'Bank':
            pass
        elif self.name == 'Giant Statue':
            pass
    
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

commonBuildings =  (Building('Brick House', 1, 1,  'Brick House', 'Common', (5,0), (0,0), 'Brick House\n--------------\n+ 5 Score\nwhen activated.'),
                    Building('Log House', 1, 1,  'Log House', 'Common', (5,0), (0,0), 'Log House\n--------------\n+ 5 Score\nwhen activated.'),
                    Building('Modern House', 1, 1, 'Modern House', 'Common', (5,0), (0,0), 'Modern House\n--------------\n+ 5 Score\nwhen activated.'),
                    Building('Farm', 2, 1,  'Barn', 'Common', (10,0), (0,0), 'Farm\n--------------\n+ 10 Score\nwhen activated.'),
                    Building('Crop Field', 1, 1,  'Crop Field', 'Common', (0,0), (1,0), 'Crop Field\n--------------\n+ $1\nwhen activated.'),
                    Building('School', 2, 1, 'School', 'Common', (10,0), (0,0), 'School\n--------------\n+ 10 Score\nwhen activated.\nDoubles score of\nadjacent buildings.'))

uncommonBuildings = (Building('Condo', 3, 2,  'Condo', 'Uncommon', (10,0), (0,0), 'Condo\n--------------\n+ 10 Score\nwhen activated.'),
                    Building('Tall House', 2, 1,  'Tall House', 'Uncommon', (10,0), (0,0), 'Tall House\n--------------\n+ 10 Score\nwhen activated.'),
                    Building('Pool', 3, 2, 'Pool', 'Uncommon', (50,0), (0,0), 'Pool\n--------------\n+ 50 Score\nwhen activated.'),
                    Building('Wind Turbine', 2, 1,  'Wind Turbine', 'Uncommon', (10,0), (0,0), 'Wind Turbine\n--------------\n+ 10 Score\nwhen activated.'),
                    Building('Bridge', 3, 2,  'Bridge', 'Uncommon', (0,0), (0,0), 'Bridge\n--------------\nRepeats the ability\nof the Building\nto the left\nwhen activated.'),
                    Building('Resturant', 4, 3, 'Resturant', 'Uncommon', (15,0), (0,0), 'Resturant\n--------------\n+ 15 Score\nwhen activated.'),
                    Building('Mine Quarry', 4, 3, 'Mine Quarry', 'Uncommon', (15,0), (0,0), 'Mine Quarry\n--------------\n+ 15 Score\nand + $1-5\nwhen activated.'))

rareBuildings = (Building('Power Plant', 5, 4,  'Power Plant', 'Rare', (30,0), (0,0), 'Power Plant\n--------------\n+ 30 Score\nwhen activated.'),
                Building('Mansion', 5, 4,  'Mansion', 'Rare', (100,0), (0,0), 'Mansion\n--------------\n+ 100 Score\nwhen activated.'),
                Building('Church', 4, 3, 'Church', 'Rare', (20,0), (0,0), 'Church\n--------------\n+ 20 Score\nwhen activated.'),
                Building('Hospital', 5, 4, 'Hospital', 'Rare', (20,0), (0,0), 'Hospital\n--------------\n+ 20 Score\nwhen activated.'),
                Building('Fire Station', 5, 4, 'Fire Station', 'Rare', (20,0), (0,0), 'Fire Station\n--------------\n+ 20 Score\nwhen activated.'),
                Building('Ferris Wheel', 4, 3, 'Ferris Wheel', 'Rare', (15,0), (0,0), 'Ferris Wheel\n--------------\n+ 20 Score\nwhen activated.'))

epicBuildings = (Building('Skyscraper', 7, 5,  'Skyscraper', 'Epic', (50,0), (0,0), 'Skyscaper\n--------------\n+ 50 Score\nwhen activated.'),
                Building('Castle', 7, 5, 'Castle', 'Epic', (75,0), (0,0), 'Castle\n--------------\n+ 75 Score\nwhen activated.'),
                Building('Casino', 8, 6, 'Casino', 'Epic', (0,0), (0,0), 'Casino\n--------------\nGives random score and money\nwhen activated.'),
                Building('Bank', 6, 4,  'Bank', 'Epic', (30,0), (0,0), 'Bank\n--------------\n+ 30 Score\nwhen activated.'),
                Building('Police Station', 6, 5,  'Police Station', 'Epic', (30,0), (0,0), 'Police Station\n--------------\n+ 30 Score\nwhen activated.'),
                Building('Airport', 6, 4,  'Airport', 'Epic', (0,0), (0,0), 'Airport\n--------------\nRepeats all\nnearby Buildings\' abilities\nwhen activated.'),)

legendaryBuildings = (Building('Pyramid', 9, 7,  'Pyramid', 'Legendary', (500,0), (0,0), 'Pyramid\n--------------\n+ 500 Score\nwhen activated.'),
                     Building('Colloseum', 8, 6,  'Colloseum', 'Legendary', (400,0), (0,0), 'Colloseum\n--------------\n+ 400 Score\nwhen activated.'),
                     Building('Space Station', 10, 8, 'Space Station', 'Legendary', (200,0), (0,0), 'Church\n--------------\n+ 200 Score\nwhen activated.'),
                     Building('Volcano', 9, 7, 'Volcano', 'Legendary', (1000,0), (0,0), 'Volcano\n--------------\n+ 1000 Score\nwhen activated.'),
                     Building('Giant Statue', 10, 8, 'Giant Statue', 'Legendary', (0,0), (0,0), 'Giant Statue\n--------------\nBuffs everything\nwhen activated.'),)

allBuildings = (commonBuildings, uncommonBuildings, rareBuildings, epicBuildings, legendaryBuildings)




