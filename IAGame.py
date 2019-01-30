import Board as Board
import  Snake as Snake
import time
import Network
from pynput import keyboard
import os
"""Program that lets the IA play snake"""
class Game:
    def __init__(self):
        self.board = Board.Board()
        self.snake = Snake.Snake()

    def status(self):
        stat = []
        for i in range(0,30):
            for j in range(0,80):
                if self.board.board[i][j] == '■':
                    stat.append(-5)
                elif self.board.board[i][j] == ' ':
                    stat.append(0)
                else:
                    stat.append(5)
        for coord in self.snake.body:
            stat[80*coord[0] + coord[1]]=1
        return stat

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


if __name__  ==  '__main__':
    network = Network.Network()
    game = Game()
    game.print()
    finished = False;
    score = 0;
    while not finished:
        time.sleep(0.05)
        input = game.status()
        move = network.takeDecision(input)
        print(move)
        if move == 0:
            game.snake.changeDirection((0,1))
        elif move == 1:
            game.snake.changeDirection((0,-1))
        elif move == 2:
            game.snake.changeDirection((1,0))
        elif move == 3:
            game.snake.changeDirection((-1,0))
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
