import random


class Board:
    def __init__(self,height, width):
        self.board = []
        self.width = width
        self.height = height
        self.fruit = (0,0)
        for i in range(0,self.height):
            self.board.append([])
            if i ==0 or i==self.height-1:
                for j in range(0,self.width):
                    self.board[i].append('■')
            else:
                self.board[i].append('■')
                for j in range(1,self.width-1):
                    self.board[i].append(' ')
                self.board[i].append('■')
        self.createFruit()

    def createFruit(self):
        self.board[self.fruit[0]][self.fruit[1]] = ' '
        fruitX = random.randint(1,self.width-2)
        fruitY = random.randint(1,self.height-2)
        self.fruit = (fruitY,fruitX)
        self.board[fruitY][fruitX] = '@'


    def printB(self):
        res = ""
        for line in self.board:
            for cell in line:
                res+=cell
            res+='\n'
        print(res)

if __name__=='__main__':
    board = Board()
    board.printB()
    board.createFruit()
    board.printB()