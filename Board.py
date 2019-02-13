import random


class Board:
    def __init__(self,height, width):
        self.fruitTab = [(15,9),(3,0),(15,1),(14,9),(6,11),(19,12),(8,8),(6,1),(4,13),(3,13),(2,2),(17,1),(4,3),(8,10),(10,18),(18,0),(11,1),(13,6),(14,7),(7,13),(11,6),(5,19),(14,4),(12,11),(17,16),(4,19),(10,1),(12,7),(16,12),(17,7),(10,7),(19,13),(0,4),(19,15),(12,6),(8,15),(13,5),(14,19),(9,6),(10,18),(14,14),(10,17),(7,2),(4,4),(7,13),(3,9),(13,14),(3,13),(19,14),(0,3),(1,8),(18,6),(6,4),(17,7),(10,8),(6,17),(14,8),(6,14),(2,2),(18,9),(15,13),(19,0),(7,2),(14,18),(8,14),(1,9),(15,11),(7,1),(15,17),(0,18),(5,18),(7,11),(6,13),(5,9),(15,15),(10,2),(8,9),(3,16),(3,9),(6,12),(3,8),(13,10),(19,13),(3,7),(10,4),(5,7),(2,12),(10,1),(17,16),(2,12),(11,12),(6,12),(14,9),(0,9),(10,6),(13,14),(6,19),(16,6),(12,0),(5,14)]
        self.fruitIndex = 0
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
        """fruitX = random.randint(1,self.width-2)
        fruitY = random.randint(1,self.height-2)
        self.fruit = (fruitY,fruitX)
        self.board[fruitY][fruitX] = '@'"""
        self.fruit = self.fruitTab[self.fruitIndex]
        self.board[self.fruit[0]][self.fruit[1]] = '@'
        self.fruitIndex+=1


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
