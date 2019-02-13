#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""TODO:
        - probabilist selection for reproduction
        - register last bests from gen in logs
        - recreation of a generation from log"""



import sys
import Network
import IAGame
import os
import random
import Board as Board
import  Snake as Snake
from pynput import keyboard

global next
class Genetics:
    def __init__(self,popsize,sizes):
        self.popSize = popsize
        self.population = [Network.Network(sizes) for i in range(0,self.popSize)]
        self.results = []
        self.bests = []
        self.genNum = 0

    def fitness(self,gameRes):
        score = gameRes[0]
        nbFrames = gameRes[1]
        return 50*score + nbFrames

    def bestOnes(self):
        nbWanted = 2
        self.bests = []
        def takeFirst(elem):
            return elem[0]
        for result in self.results:
            if len(self.bests)<0.1*self.popSize:
                self.bests.append(result)
            else:
                self.bests.sort(key=takeFirst,reverse=True)
                if result[0] > self.bests[-1][0]:
                    del self.bests[-1]
                    self.bests.append(result)
                    self.bests.sort(key=takeFirst,reverse=True)

    def createNewPop(self,bests):
        tmp=[]
        bestNeurons = [couple[1] for couple in bests]
        #random.shuffle(bestNeurons)
        for i in range(0,10):
            for par1,par2 in zip(bestNeurons[0::2],bestNeurons[1::2]):
                children = par1.reproduction(par2)
                tmp.append(children[0])
                tmp.append(children[1])
        self.population = tmp

    def mutation(self):
        for individual in self.population:
                individual.mutate()

    def playOneGen(self,height,width):
        game = IAGame.Game(height,width)
        self.results = []
        for network in self.population:
            score = 0
            nbFrames = 0
            finished = False
            while not finished and nbFrames < 1000:
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
                nbFrames+=1
                if (game.hasEaten()):
                    game.snake.grow()
                    game.board.createFruit()
                    score += 1
                if game.end():
                    finished = True
            self.results.append([self.fitness([score,nbFrames]),network])
            game.reset()
        self.genNum+=1


def on_press(key):
    global next
    if key == keyboard.Key.up:
        next = True

if __name__=='__main__':
    fit = []
    bestEver = []
    nbGenerationToRun = 300
    GenerationSize = 200
    height = 20
    width = 20
    help = 'This programm is a genetic algorithm trying to play snake\n'
    help += 'python3 Genetics.py [option] <argument>\n'
    help += 'List of options:\n'
    help += ' --help : show this window\n'
    help += '    -n : number of generations to train on\n'
    help += '    -s : number of individuals in a generation\n'
    help += '    -h : height of the board\n'
    help += '    -w : width of the board\n'
    help+= 'Example: python3 Genetics.py -n 10 -s 100'
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        print (help)
        sys.exit()
        """if len(sys.argv) == 3:
            if sys.argv[1] == '-n':
                try:
                    nbGenerationToRun = int(sys.argv[2])
                except:
                    print('Argument must be an integer\n')
                    sys.exit()
            elif sys.argv[1] == 's':
                try:
                    GenerationSize= int(sys.argv[2])
                except:
                    print('Argument must be an integer\n')
                    sys.exit()
        if len(sys.argv) == 5:
            try:
                if sys.argv[1] == '-n' and sys.argv[3] == '-s':
                    nbGenerationToRun = int(sys.argv[2])
                    GenerationSize = int(sys.argv[4])
                elif sys.argv[3] == '-n' and sys.argv[1] == '-s':
                    nbGenerationToRun = int(sys.argv[4])
                    GenerationSize = int(sys.argv[2])
                else:
                    print('Wrong arguments format. Call --help for expected format.')
                    sys.exit()
            except:
                print('Argument must be an integer\n')
                sys.exit()
        elif  len(sys.arv) != 0:
            print('Wrong arguments format. Call --help for expected format.')
            sys.exit()"""
    else:
        for i in range(1,len(sys.argv)-1):
            try:
                opt = sys.argv[i]
                if opt == '-h':
                    height = int(sys.argv[i+1])
                elif opt == '-w':
                    width = int(sys.argv[i+1])
                elif opt == '-n':
                    nbGenerationToRun = int(sys.argv[i+1])
                elif opt == '-s':
                    GenerationSize = int(sys.argv[i+1])
            except:
                print('Argument must be an integer\n')
                sys.exit()
    gen = Genetics(GenerationSize,[height*width,30,4])
    print(nbGenerationToRun)
    os.system('rm -rf Logs')
    os.system('mkdir Logs')
    for i in range(0,nbGenerationToRun):
        if i % 10 ==0:
            os.system('mkdir Logs/Generation{}'.format(i))
    os.system('mkdir Logs/Generation{}'.format(nbGenerationToRun-1))
    for i in range(0,nbGenerationToRun):
        print("Generation numero: {}".format(i))
        gen.playOneGen(height,width)
        gen.bestOnes()
        gen.createNewPop(gen.bests)
        gen.mutation()
        print(len(gen.population))
        average = 0
        for result in gen.bests:
            average+=result[0]
            if i % 10 ==0 or i==nbGenerationToRun-1:
                print('Fitness: {}\n'.format(result[0]))
        print("Average fitness: {} ".format(average/len(gen.bests)))	
        fit.append(average/len(gen.bests))
            #os.system('gedit Logs/Generation{}/result.log &'.format(gen.genNum-1))
    with open('fitresult.log','w') as file:
        file.write(str(fit))
    for best in gen.bests:
        bestEver.append(best)
    global next
    next = False
    with keyboard.Listener(on_press=on_press) as listener:
        for element in bestEver:
            network = element[1]
            game = IAGame.Game(height,width)
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
                #os.system('clear')
                game.printG()
                while not next:
                    pass
                next = False
                print(score)
            os.system('clear')
