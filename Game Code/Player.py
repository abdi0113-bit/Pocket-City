import pygame
import random

import Buildings

class Player():
    def __init__(self, name, turn, boardSize):
        self.name = name
        self.turn = turn

        #
        self.score = 0
        self.money = 0

        # Initialise shop and board
        self.board = [[None for j in range(boardSize[0])] for i in range(boardSize[1])]
        self.board[int(boardSize[1]/2)][int(boardSize[0]/2)] = Buildings.starterTent
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
    
