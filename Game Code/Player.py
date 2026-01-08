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
        self.lives = 10

        # Initialise shop and board
        self.board = [[None for j in range(boardSize[0])] for i in range(boardSize[1])]
        self.board[int(boardSize[1]/2)][int(boardSize[0]/2)] = Buildings.starterTent
        self.shop = []
        self.rerollShop(1, 3)

        # Cost of expanding the board
        self.expandCost = 4

    def canAfford(self, cost):
        return self.money >= cost

    def spendMoney(self, cost):
        if self.canAfford(cost):
            self.money -= cost
            return True
        return False
    
    def rerollShop(self, roundNum, shopLength):
        # Percentages of each rarity, order is C, U, R, E, L
        rarityDistribution = (
            (1.00, 0.00, 0.00, 0.00, 0.00),
            (1.00, 0.00, 0.00, 0.00, 0.00),
            (0.70, 0.30, 0.00, 0.00, 0.00),
            (0.60, 0.40, 0.00, 0.00, 0.00),
            (0.40, 0.50, 0.10, 0.00, 0.00),
            (0.30, 0.50, 0.20, 0.00, 0.00),
            (0.20, 0.45, 0.25, 0.10, 0.00),
            (0.20, 0.35, 0.30, 0.15, 0.00),
            (0.10, 0.25, 0.35, 0.20, 0.10)
        )

        self.shop = []
        for i in range(shopLength):
            rarityToUse = 0

            roundNumAdjusted = roundNum
            if roundNumAdjusted >= len(rarityDistribution):
                # Use the distribution for the last programmed round if round number is bigger
                roundNumAdjusted = len(rarityDistribution) - 1
            
            rarityRoll = random.random()
            
            # Finds the right rarity based on roll
            for rarity in range(5):
                rarityRoll -= rarityDistribution[roundNumAdjusted][rarity]
                if rarityRoll < 0:
                    rarityToUse = rarity
                    break

            buildingsDict = Buildings.allBuildings[rarityToUse]
            self.shop.append(random.choice(list(buildingsDict.values()))) # This is how to get a random item from a dictionary    
