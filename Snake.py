
"""
This module defines the behavior of the snake
"""

class Snake:
    # Initializes the snake at the center of the board, heading right
    def __init__(self, height, width):
        posy = height//2
        posx = width//2
        self.direction = (0, 1)
        self.body = [(posy, posx)]
        self.body+=[(self.body[0][0]-self.direction[0],self.body[0][1]-self.direction[1])]
        self.body += [(self.body[1][0] - self.direction[0], self.body[1][1] - self.direction[1])]

    # Retuns true if the current postition is on the snake's body
    def isBody(self,pos):
        for coord in self.body:
            if coord[0] == pos[0] and coord[1] == coord[1] and pos != self.head():
                return True
        return False

    # "Grows" the snake. Creates a new body part at its end
    def grow(self):
        length = len(self.body)
        last = self.body[length-1]
        bLast = self.body[length-2]
        dx = last[1] - bLast[1]
        dy = last[0] - bLast[0]
        self.body.append((last[0]+dy,last[1]+dx))

    # Updates current direction for the one passed as parameter. Returns true if the direction has changed
    def changeDirection(self, dir):
        changed = False
        if not (self.direction[0] + dir[0] == 0 and self.direction[1] + dir[1] == 0):
            if self.direction[0] != dir[0] or self.direction[1] != dir[1]:
                changed = True
            self.direction = dir
        return changed

    # Moves the snake. Displaces all its parts towards the right direction
    def move(self):
        head = self.body[0]
        self.body.pop(len(self.body)-1)
        self.body.insert(0,(head[0]+self.direction[0],head[1]+self.direction[1]))

    def head(self):
        return self.body[0]
    # Returns the length of the snake's body
    def length(self):
        return len(self.body)

    # Looks in one direction (vect) in the board. Returns a list containing the inversed distance separating the
    # Snake from : the fruit, itself, a wall
    def lookOneDir(self,vect, board):
        pos= [x for x in self.head()]
        res = [0, 0, 0]
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

    # Returns the result of the snake looking in each of 8 directions
    def lookAllDir(self,board):
        view = [0]*24
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

# I guess I just needed a function to copy an array into another
def copy(tab1, tab2, offset):
    for i in range(0,len(tab1)):
        tab2[i+offset] = tab1[i]


if __name__=='__main__':
    print("This module is not to be called. Call Genetics.py instead")
    exit()
