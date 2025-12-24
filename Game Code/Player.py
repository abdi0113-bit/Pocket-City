import pygame
import random

import Buildings

class Player():
    def __init__(self, money, name, score, turn):
        self.money = money
        self.name = name
        self.score = score
        self.turn = turn

        # Initialise shop and board
        self.board = [[None for j in range(3)] for i in range(3)]
        self.board[1][1] = Buildings.starterTent
        self.shop = []
        self.rerollShop(1)

    def canAfford(self, cost):
        return self.money >= cost

    def spendMoney(self, cost):
        if self.canAfford(cost):
            self.money -= cost
            return True
        return False
    
    def rerollShop(self, roundNum):
        self.shop = []
        for i in range(3):
            self.shop.append(random.choice(Buildings.commonBuildings))
    
