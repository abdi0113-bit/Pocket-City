import pygame

class Building():
    def __init__(self, name, cost, image, rarity):
        self.name = name
        self.cost = cost
        self.image = image
        self.rarity = rarity

    def whenActivated(self):
        if self.name == 'Brick House':
            pass
        elif self.name == 'Log House':
            pass

    def whenPlaced(self):
        if self.name == 'Brick House':
            pass
        elif self.name == 'Log House':
            pass

    def whenBought(self, currentMoney):
        if self.name == 'Brick House':
            pass
        elif self.name == 'Log House':
            pass

        return currentMoney - self.cost
    


commonBuildings = [Building('Brick House', 5,  'Brick House', 'Common'),
                   Building('Log House', 4,  'Log House', 'Common'),
                   Building('Modern House', 6, 'Modern House', 'Common')]
uncommonBuildings = []
rareBuildings = []
epicBuildings = []
legendaryBuildings = []