import pygame
import random
import copy
import datetime

import Buildings

class Player():
    def __init__(self, name, turn, boardSize):
        self.name = name
        self.turn = turn

        # Initialise currencies
        self.score = 0
        self.money = 0
        self.lives = 10
        self.charge = 0

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
            randomBuilding = copy.copy(random.choice(list(buildingsDict.values())))

            # Nothing to see here! You don't understand this code! Moving right along!
            if datetime.date.today().month == 4 and datetime.date.today().day == 1:
                if random.random() < 0.1:
                    randomBuilding = Buildings.easterEgg
            
            # Add new items to the shop if the shop isn't long enough
            if i >= len(self.shop):
                self.shop.append(randomBuilding) # This is how to get a random item from a dictionary
            
            else:
                # Otherwise, relace existing items if not frozen
                if not self.shop[i].frozen:
                    self.shop[i] = randomBuilding
                else:
                    pass
                    #debugItem = Buildings.legendaryBuildings['Giant Statue']
                    #self.shop[i] = copy.copy(debugItem)