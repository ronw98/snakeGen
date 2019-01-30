import Board as Board
import  Snake as Snake
import time
from pynput import keyboard
import os
class Game:
    def __init__(self):
        self.board = Board.Board()
        self.snake = Snake.Snake()

    def print(self):
        disp =  []
        for j in range(0,30):
            disp.append([])
            for i in range(0,80):
                disp[j].append(' ')
        res = ""
        for i in range(0,30):
            for j in range(0,80):
                disp[i][j] = self.board.board[i][j]
        for coord in self.snake.body:
            disp[coord[0]][coord[1]] = '●'
        for line in disp:
            for cell in line:
                res+=cell
            res+='\n'
        print(res)

    def hasEaten(self):
        return self.snake.body[0]==self.board.fruit

    def end(self):
        head = self.snake.body[0]
        if head[1] >=79 or head[0] >= 29:
            return True
        if head[1] <0 or head[0] < 0:
            return True
        for i in range(1,len(self.snake.body)):
            if head == self.snake.body[i]:
                return True


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
    game = Game()
    game.print()
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
            game.print()
            print(score)
