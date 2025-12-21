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