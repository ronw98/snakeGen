import random


class Board:
    def __init__(self,height, width):
        self.fruitTab = [(20,26),(11,18),(27,27),(3,3),(21,11),(20,19),(8,17),(23,18),(1,24),(26,26),(4,16),(18,9),(21,24),(9,5),(21,27),(10,12),(8,5),(2,7),(3,16),(9,8),(26,28),(26,18),(16,5),(19,16),(28,1),(26,3),(28,15),(11,20),(22,3),(9,26),(13,2),(9,20),(6,22),(26,21),(22,6),(28,3),(17,9),(20,17),(25,23),(16,24),(23,13),(26,6),(11,20),(10,16),(22,18),(13,18),(19,6),(10,9),(11,19),(1,4),(9,12),(7,25),(4,10),(13,1),(4,1),(24,10),(25,6),(16,20),(9,25),(7,15),(14,4),(4,16),(9,13),(24,19),(4,24),(7,12),(19,13),(20,23),(22,17),(23,10),(1,2),(19,25),(7,18),(16,16),(14,7),(14,11),(10,17),(11,18),(14,18),(20,17),(26,26),(12,16),(22,15),(10,28),(3,16),(9,3),(18,11),(12,8),(1,11),(7,26),(17,20),(21,10),(9,15),(27,6),(4,3),(6,1),(28,17),(17,6),(15,10),(5,18)]
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
        if random.randint(0,1) ==0:
            fruitX = random.randint(1,self.width-2)
            fruitY = random.randint(1,self.height-2)
            self.fruit = (fruitY,fruitX)
            self.board[fruitY][fruitX] = '@'
        else:
            if self.fruitIndex >= 100:        
                fruitX = random.randint(1,self.width-2)
                fruitY = random.randint(1,self.height-2)
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
