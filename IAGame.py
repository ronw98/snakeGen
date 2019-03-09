#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Board as Board
import  Snake as Snake
import os
import time

"""Program that lets the IA play snake"""
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

    # Lets the given neural network play one game, returns the number of frames and score obtained
    def play(self,network, watched=False,frameRate=0.1):
        score = 0
        nbFrames = 0
        nextToWall = 0
        tNotEat = 0
        finished = False
        while (not finished) and tNotEat < 100 and nbFrames < 5000:
            input = self.snake.lookAllDir(self.board)
            move = network.takeDecision(input)
            if move == 0:
                self.snake.changeDirection((0, 1))
            elif move == 1:
                self.snake.changeDirection((0, -1))
            elif move == 2:
                self.snake.changeDirection((1, 0))
            elif move == 3:
                self.snake.changeDirection((-1, 0))
            self.snake.move()
            nbFrames += 1
            tNotEat += 1
            if self.snake.head()[0] >= self.board.height - 2 or self.snake.head()[0] <= 1 or self.snake.head()[
                1] >= self.board.width - 2 or self.snake.head()[1] <= 1:
                nextToWall += 1
            if self.hasEaten():
                self.snake.grow()
                self.board.createFruit()
                score += 1
                tNotEat = 0
            if self.end():
                finished = True
            if watched:
                time.sleep(frameRate)
                os.system('clear')
                self.printG()
                print(score)
        self.reset()
        if not watched:
            return score,nbFrames


if __name__  ==  '__main__':
    print("This module is not to be called. Call Genetics.py instead")
    exit()

