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
        if self.name == 'Brick House':
            pass
        elif self.name == 'Log House':
            pass

        # This will automatically deal with increasing score and money
        return self.scoreIncreaseActivate, self.moneyIncreaseActivate

    def whenPlaced(self):
        # These are any custom abilities, placeholders for now
        if self.name == 'Brick House':
            pass
        elif self.name == 'Log House':
            pass

        # This will automatically deal with increasing score and money
        return self.scoreIncreasePlace, self.moneyIncreasePlace

    def whenBought(self, currentMoney):
        # UNUSED FOR NOW
        # These are any custom abilities, placeholders for now
        if self.name == 'Brick House':
            pass
        elif self.name == 'Log House':
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
         

starterTent = Building('Starter Tent', 5, 1,  'Starter Tent', '', (1,0), (0,0), 'Starter Tent\n--------------\nIncreases score\nby 1 when\nactivated.')

commonBuildings =  [Building('Brick House', 5, 4,  'Brick House', 'Common', (10,0), (0,0), 'Mouseover text'),
                    Building('Log House', 4, 3,  'Log House', 'Common', (6,0), (0,0), 'Placeholder text'),
                    Building('Modern House', 7, 5, 'Modern House', 'Common', (0,0), (10,0), 'Cool text')]
uncommonBuildings = []
rareBuildings = []
epicBuildings = []
legendaryBuildings = []