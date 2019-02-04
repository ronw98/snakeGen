#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Board as Board
import  Snake as Snake
import time
import Network
import os
"""Program that lets the IA play snake"""
class Game:
    def __init__(self):
        self.board = Board.Board()
        self.snake = Snake.Snake(self.board.height,self.board.width)

    def status(self):
        stat = []
        stat.append(self.snake.head()[0])
        stat.append(self.snake.head()[1])
        stat.append(self.snake.mid()[0])
        stat.append(self.snake.mid()[1])
        stat.append(self.snake.tail()[0])
        stat.append(self.snake.tail()[1])
        stat.append(self.snake.turns())
        stat.append(self.snake.length())
        stat.append(self.snake.direction[0])
        stat.append(self.snake.direction[1])
        stat.append(self.board.fruit[0])
        stat.append(self.board.fruit[1])
        stat.append(self.board.width)
        stat.append(self.board.height)
        return stat

    def printG(self):
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
        if head[1] <=0 or head[0] <=0:
            return True
        for i in range(1,len(self.snake.body)):
            if head == self.snake.body[i]:
                return True

    def reset(self):
        self.board= Board.Board()
        self.snake=Snake.Snake(self.board.height,self.board.width)

    def play(self,network):
        finished = False;
        score = 0
        nbFrames = 0
        while not finished:
            nbFrames+=1
            input = game.status()
            move = network.takeDecision(input)
            if move == 0:
                game.snake.changeDirection((0, 1))
            elif move == 1:
                game.snake.changeDirection((0, -1))
            elif move == 2:
                game.snake.changeDirection((1, 0))
            elif move == 3:
                game.snake.changeDirection((-1, 0))
            game.snake.move()
            if (game.hasEaten()):
                game.snake.grow()
                game.board.createFruit()
                score += 1
            if game.end():
                finished = True
        return (score,nbFrames)


if __name__  ==  '__main__':
    network = Network.Network()
    game = Game()
    game.printG()
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
        game.printG()
        print(score)
