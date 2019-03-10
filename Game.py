import Board as Board
import  Snake as Snake
import time
from pynput import keyboard
import os
class Game:
    def __init__(self,height,width):
        self.board = Board.Board(height,width)
        self.snake = Snake.Snake(self.board.height,self.board.width)

    # Displays the game (yup, it should return the string containing the game)
    def printG(self):
        disp =  []
        for j in range(0,self.board.height):
            disp.append([])
            for i in range(0,self.board.width):
                disp[j].append(' ')
        res = ""
        for i in range(0,self.board.height):
            for j in range(0,self.board.width):
                disp[i][j] = self.board.board[i][j]
        for coord in self.snake.body:
            disp[coord[0]][coord[1]] = '●'
        for line in disp:
            for cell in line:
                res+=cell
            res+='\n'
        print(res)

    # Returns true if the snake is eating a fruit
    def hasEaten(self):
        return self.snake.body[0]==self.board.fruit

    # Returns true if the snake is dead
    def end(self):
        """head = self.snake.body[0]
        if head[1] >=self.board.height-2 or head[0] >= self.board.width-2:
            return True
        if head[1] <=1 or head[0] <=1:
            return True
        for i in range(1,len(self.snake.body)):
            if head == self.snake.body[i]:
                return True""" # This is to be removed
        return self.board.isWall(self.snake.head()) or self.snake.isBody(self.snake.head())
    # Resets the game to the begining
    def reset(self):
        self.board= Board.Board(self.board.height,self.board.width)
        self.snake=Snake.Snake(self.board.height,self.board.width)


def on_press(key):
    global game
    print(key)
    if key == keyboard.Key.up:
        game.snake.changeDirection((-1, 0))
        print("ok")
    elif key == keyboard.Key.down:
        game.snake.changeDirection((1, 0))
    elif key == keyboard.Key.right:
        game.snake.changeDirection((0,1))
    elif key == keyboard.Key.left:
        game.snake.changeDirection((0,-1))

if __name__  ==  '__main__':
    global game
    game = Game(30,30)
    game.printG()
    finished = False;
    score = 0;
    with keyboard.Listener(on_press=on_press
           ) as listener:
        while not finished:
            time.sleep(0.05)
            game.snake.move()
            if(game.hasEaten()):
                game.snake.grow()
                game.board.createFruit()
                score+=1
            if game.end():
                finished = True
            os.system('clear')
            game.printG()
            print(score)
