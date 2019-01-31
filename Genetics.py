#!/usr/bin/env python
# -*- coding: utf-8 -*-


import Network
import IAGame
import os
import Board as Board
import  Snake as Snake

class Genetics:
    def __init__(self):
        self.popSize = 200
        self.population = [Network.Network() for i in range(0,self.popSize)]
        self.results = []

    def fitness(self,gameRes):
        score = gameRes[0]
        nbFrames = gameRes[1]
        return 20*score + nbFrames

    def bestOnes(self):
        nbWanted = 20
        bests = []
        def takeFirst(elem):
            return elem[0]
        for result in self.results:
            if len(bests)<20:
                bests.append(result)
            else:
                bests.sort(key=takeFirst,reverse=True)
                if result[0] > bests[-1][0]:
                    del bests[-1]
                    bests.append(result)
        return bests

    def createNewPop(self,bests):
        tmp=[]
        bestNeurons = [couple[1] for couple in bests]
        for i in range(0,10):
            for par1,par2 in zip(bestNeurons[0::2],bestNeurons[1::2]):
                children = par1.reproduction(par2)
                tmp.append(children[0])
                tmp.append(children[1])
        self.population = tmp

    def playOneGen(self):
        game = IAGame.Game()
        for network in self.population:
            score = 0
            nbFrames = 0
            finished = False
            while not finished:
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
            self.results.append([self.fitness([score,nbFrames]),network])
            game.reset()


if __name__=='__main__':
    gen = Genetics()
    for i in range(0,10):
        print("Generation numero: {}".format(i))
        gen.playOneGen()
        gen.createNewPop(gen.bestOnes())
    bests = gen.bestOnes()
    print(bests[0])
    network = bests[0][1]
    game = IAGame.Game()
    game.printG()
    finished = False;
    score = 0;
    while not finished:
        input = game.status()
        move = network.takeDecision(input)
        print(move)
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
        os.system('clear')
        game.printG()
        print(score)