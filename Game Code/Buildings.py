import pygame

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
        if self.name == 'Resturant':
            pass
        elif self.name == 'Casino':
            pass

        # This will automatically deal with increasing score and money
        return self.scoreIncreaseActivate, self.moneyIncreaseActivate

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

    def whenBought(self, currentMoney):
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
        # Return the current money minus the cost
        return currentMoney - self.cost
    
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
         

starterTent = Building('Starter Tent', 1, 1,  'Starter Tent', '', (1,0), (0,0), 'Starter Tent\n--------------\nIncreases score by 1\nWhen Activated.')

commonBuildings =  [Building('Brick House', 1, 1,  'Brick House', 'Common', (5,0), (0,0), 'Brick House\n--------------\nIncreases score by 5\nWhen Activated.'),
                    Building('Log House', 1, 1,  'Log House', 'Common', (5,0), (0,0), 'Log House\n--------------\nIncreases score by 5\nWhen Activated.'),
                    Building('Modern House', 1, 1, 'Modern House', 'Common', (5,0), (0,0), 'Modern House\n--------------\nIncreases score by 5\nWhen Activated.'),
                    Building('Farm', 2, 1,  'Barn', 'Common', (10,0), (0,0), 'Farm\n--------------\nIncreases score by 10\nWhen Activated.'),
                    Building('Crop Field', 1, 1,  'Crop Field', 'Common', (0,0), (1,0), 'Crop Field\n--------------\nIncreases coins by 1\nWhen Activated.'),
                    Building('School', 2, 1, 'School', 'Common', (10,0), (0,0), 'School\n--------------\nIncreases score by 10\nWhen Activated.')]

uncommonBuildings = [Building('Condo', 3, 2,  'Condo', 'Uncommon', (10,0), (0,0), 'Condo\n--------------\nIncreases score by 10\nWhen Activated.'),
                    Building('Tall House', 2, 1,  'Tall House', 'Uncommon', (10,0), (0,0), 'Tall House\n--------------\nIncreases score by 10\nWhen Activated.'),
                    Building('Pool', 3, 2, 'Pool', 'Uncommon', (50,0), (0,0), 'Pool\n--------------\nIncreases score by 50\nWhen Activated.'),
                    Building('Wind Turbine', 2, 1,  'Wind Turbine', 'Uncommon', (10,0), (0,0), 'Wind Turbine\n--------------\nIncreases score by 10\nWhen Activated.'),
                    Building('Bridge', 3, 2,  'Bridge', 'Uncommon', (0,0), (0,0), 'Bridge\n--------------\nRepeats the Last Buildings Abilities\nWhen Activated.'),
                    Building('Resturant', 4, 3, 'Resturant', 'Uncommon', (15,0), (0,0), 'Resturant\n--------------\nIncreases score by 15\nWhen Activated.'),
                    Building('Mine Quarry', 4, 3, 'Mine Quarry', 'Uncommon', (15,0), (0,0), 'Mine Quarry\n--------------\nIncreases score by 15\nWhen Activated.')]

rareBuildings = [Building('Power Plant', 5, 4,  'Power Plant', 'Rare', (30,0), (0,0), 'Power Plant\n--------------\nIncreases score by 30\nWhen Activated.'),
                Building('Mansion', 5, 4,  'Mansion', 'Rare', (100,0), (0,0), 'Mansion\n--------------\nIncreases score by 100\nWhen Activated.'),
                Building('Church', 4, 3, 'Church', 'Rare', (20,0), (0,0), 'Church\n--------------\nIncreases score by 20\nWhen Activated.'),
                Building('Hospital', 5, 4, 'Hospital', 'Rare', (20,0), (0,0), 'Hospital\n--------------\nIncreases score by 20\nWhen Activated.'),
                Building('Fire Station', 5, 4, 'Fire Station', 'Rare', (20,0), (0,0), 'Fire Station\n--------------\nIncreases score by 20\nWhen Activated.'),
                Building('Ferris Wheel', 4, 3, 'Ferris Wheel', 'Rare', (15,0), (0,0), 'Ferris Wheel\n--------------\nIncreases score by 20\nWhen Activated.')]

epicBuildings = [Building('Skyscraper', 7, 5,  'Skyscraper', 'Epic', (50,0), (0,0), 'Skyscaper\n--------------\nIncreases score by 50\nWhen Activated.'),
                Building('Castle', 7, 5, 'Castle', 'Epic', (75,0), (0,0), 'Castle\n--------------\nIncreases score by 75\nWhen Activated.'),
                Building('Casino', 8, 6, 'Casino', 'Epic', ((1 - 1000000),0), (0,0), 'Casino\n--------------\nIncreases score by random 1 - 1000000 \nWhen Activated.'),
                Building('Bank', 6, 4,  'Bank', 'Epic', (30,0), (0,0), 'Bank\n--------------\nIncreases score by 30\nWhen Activated.'),
                Building('Police Station', 6, 5,  'Police Station', 'Epic', (30,0), (0,0), 'Police Station\n--------------\nIncreases score by 30\nWhen Activated.'),
                Building('Airport', 6, 4,  'Airport', 'Epic', (0,0), (0,0), 'Airport\n--------------\nRepeats all Buildings Abilities Nearby\nWhen Activated.'),]


legendaryBuildings = [Building('Pyramid', 9, 7,  'Pyramid', 'Legendary', (500,0), (0,0), 'Pyramid\n--------------\nIncreases score by 500\nWhen Activated.'),
                     Building('Colloseum', 8, 6,  'Colloseum', 'Legendary', (400,0), (0,0), 'Colloseum\n--------------\nIncreases score by 400\nWhen Activated.'),
                     Building('Space Station', 10, 8, 'Space Station', 'Legendary', (200,0), (0,0), 'Church\n--------------\nIncreases score by 200\nWhen Activated.'),
                     Building('Volcano', 9, 7, 'Volcano', 'Legendary', (1000,0), (0,0), 'Volcano\n--------------\nIncreases score by 1000\nWhen Activated.'),
                     Building('Giant Statue', 10, 8, 'Giant Statue', 'Legendary', (0,0), (0,0), 'Giant Statue\n--------------\nIBuffs Everything\nWhen Activated.'),]

