import random
import Board
class Snake:
    def __init__(self,height,width):
        posy = height//2
        posx = width//2
        dirx = random.randint(-1,1)
        diry = 0
        if dirx == 0:
            i = random.randint(0,1)
            diry = 1
            if i == 0:
                diry = -1
        self.direction = (diry,dirx)
        self.body = [(posy,posx)]
        self.body+=[(self.body[0][0]-self.direction[0],self.body[0][1]-self.direction[1])]
        self.body += [(self.body[1][0] - self.direction[0], self.body[1][1] - self.direction[1])]

    def isBody(self,pos):
        for coord in self.body:
            if coord[0] == pos[0] and coord[1] == coord[1]:
                return True
        return False

    def grow(self):
        length = len(self.body)
        last = self.body[length-1]
        bLast = self.body[length-2]
        dx = last[1] - bLast[1]
        dy = last[0] - bLast[0]
        self.body.append((last[0]+dy,last[1]+dx))

    def changeDirection(self, dir):
        changed = False
        if not (self.direction[0] + dir[0] == 0 and self.direction[1] + dir[1] == 0):
            if self.direction[0] != dir[0] or self.direction[1] != dir[1]:
                changed = True
            self.direction = dir
        return changed

    def move(self):
        head = self.body[0]
        self.body.pop(len(self.body)-1)
        self.body.insert(0,(head[0]+self.direction[0],head[1]+self.direction[1]))
    def mid(self):
        return self.body[int(len(self.body)/2)]
    def head(self):
        return self.body[0]
    def tail(self):
        return self.body[-1]
    def turns(self):
        turn = 0
        for i in range(1,len(self.body)-2):
            if self.body[i-1][0] != self.body[i+1][0] and self.body[i-1][1] != self.body[i+1][1]:
                turn+=1
        return turn
    def length(self):
        return len(self.body)

    def lookOneDir(self,vect, board):
        pos= [x for x in self.head()]
        res = [0,0,0]
        distance = 1
        pos[0] += vect[0]
        pos[1] += vect[1]
        foundFood = foundSnake= False
        while not board.isWall(pos):
            if not foundFood and board.isFruit(pos):
                foundFood = True
                res[0] = 1/distance
            if not foundSnake and self.isBody(pos):
                foundSnake = True
                res[1] = 1/distance
            distance += 1
            pos[0] += vect[0]
            pos[1] += vect[1]
        res[2] = 1/distance
        return res

    def lookAllDir(self,board):
        view = [0 for i in range(0,24)]
        tmp = self.lookOneDir((-1,-1),board)
        copy(tmp,view,0)
        tmp = self.lookOneDir((-1, 0), board)
        copy(tmp, view, 3)
        tmp = self.lookOneDir((-1, 1), board)
        copy(tmp, view, 6)
        tmp = self.lookOneDir((0, -1), board)
        copy(tmp, view, 9)
        tmp = self.lookOneDir((0, 1), board)
        copy(tmp, view, 12)
        tmp = self.lookOneDir((1, -1), board)
        copy(tmp, view, 15)
        tmp = self.lookOneDir((1, 0), board)
        copy(tmp, view, 18)
        tmp = self.lookOneDir((1, 1), board)
        copy(tmp, view, 21)
        return view

def copy(tab1, tab2, offset):
    for i in range(0,len(tab1)):
        tab2[i+offset] = tab1[i]



