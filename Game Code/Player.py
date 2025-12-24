import pygame

class Player():
    def __init__(self, currentmoney, name, score, turn, board):
        self.money = currentmoney
        self.name = name
        self.score = score
        self.turn = turn
        self.board = board

    def spendMoney(self, cost):
        if self.money >= cost:
            self.money -= cost
            return True
        return False
    
    
