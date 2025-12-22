import pygame

class Player():
    def __init__(self, currentmoney, name, health, turn):
        self.money = currentmoney
        self.name = name
        self.health = health
        self.turn = turn

    def canAfford(self, cost):
        return self.money >= cost

    def spendMoney(self, cost):
        if self.canAfford(cost):
            self.money -= cost
            return True
        return False
    
    def isAlive(self):
        return self.health > 0
    
    
