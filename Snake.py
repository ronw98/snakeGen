import random
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

    def grow(self):
        length = len(self.body)
        last = self.body[length-1]
        bLast = self.body[length-2]
        dx = last[1] - bLast[1]
        dy = last[0] - bLast[0]
        self.body.append((last[0]+dy,last[1]+dx))

    def changeDirection(self, dir):
        if not (self.direction[0] + dir[0] == 0 and self.direction[1] + dir[1] == 0):
            self.direction = dir

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



