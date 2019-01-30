class Snake:
    def __init__(self):
        self.body = [(20,20)]
        self.body+=[(20,19)]
        self.body+=[(20,18)]
        self.direction = (0,1)

    def grow(self):
        length = len(self.body)
        last = self.body[length-1]
        bLast = self.body[length-2]
        dx = last[1] - bLast[1]
        dy = last[0] - bLast[0]
        self.body.append((last[0]+dy,last[1]+dx))

    def changeDirection(self, dir):
        if not (self.direction[0] + dir[0] == 0 and self.direction[1] + dir[1] == 1):
            self.direction = dir

    def move(self):
        head = self.body[0]
        self.body.pop(len(self.body)-1)
        self.body.insert(0,(head[0]+self.direction[0],head[1]+self.direction[1]))



