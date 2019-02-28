import random


class Board:
    def __init__(self,height, width):
        #self.fruitTab = [(10,15),(9,12),(13,14),(3,1),(18,10),(5,3),(12,5),(11,3),(14,2),(16,10),(14,9),(3,6),(14,7),(5,11),(19,19),(16,15),(14,5),(13,5),(15,13),(2,13),(19,6),(15,11),(7,7),(10,1),(8,3),(11,18),(11,13),(1,5),(16,2),(13,15),(2,9),(8,12),(10,17),(16,6),(10,18),(18,6),(1,11),(13,8),(14,3),(8,18),(5,15),(16,16),(6,16),(17,2),(17,7),(17,15),(15,2),(8,3),(18,1),(8,6),(15,3),(11,16),(10,2),(1,4),(4,5),(2,6),(1,14),(18,6),(7,12),(4,5),(19,17),(16,11),(18,1),(13,17),(2,1),(19,16),(1,10),(12,10),(11,12),(14,12),(17,12),(14,14),(7,12),(16,10),(4,19),(14,3),(17,8),(14,12),(8,4),(6,9),(2,5),(3,2),(12,11),(8,19),(1,18),(8,17),(11,2),(8,14),(13,4),(4,14),(19,15),(16,13),(19,7),(3,7),(11,8),(13,12),(13,15),(10,2),(6,17),(1,6)]
        self.fruitIndex = 100
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
        if self.fruitIndex >= 100:        
            fruitX = random.randint(4,self.width-5)
            fruitY = random.randint(4,self.height-5)
            self.fruit = (fruitY,fruitX)
            self.board[fruitY][fruitX] = '@'
        else:
            self.fruit = self.fruitTab[self.fruitIndex]
            self.board[self.fruit[0]][self.fruit[1]] = '@'
            self.fruitIndex+=1

    def isWall(self, pos):
        return self.board[pos[0]][pos[1]] == '■'
    def isFruit(self, pos):
        return self.board[pos[0]][pos[1]] == '@'

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
