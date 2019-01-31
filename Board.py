import random


class Board:
    def __init__(self):
        self.board = []
        self.fruit = (20,22)
        for i in range(0,30):
            self.board.append([])
            if i ==0 or i==29:
                for j in range(0,80):
                    self.board[i].append('■')
            else:
                self.board[i].append('■')
                for j in range(1,79):
                    self.board[i].append(' ')
                self.board[i].append('■')
        self.createFruit()

    def createFruit(self):
        self.board[self.fruit[0]][self.fruit[1]] = ' '
        fruitX = random.randint(1,78)
        fruitY = random.randint(1,28)
        self.fruit = (fruitY,fruitX)
        self.board[fruitY][fruitX] = '@'


    def print(self):
        res = ""
        for line in self.board:
            for cell in line:
                res+=cell
            res+='\n'
        print(res)

if __name__=='__main__':
    board = Board()
    board.print()
    board.createFruit()
    board.print()