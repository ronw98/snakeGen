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
import Snake as Snake
import math
import time
from pynput import keyboard
from threading import Thread, RLock
from multiprocessing import Process, Lock, Queue

lock = Lock()

def fitness(gameRes):
    score = gameRes[0]
    if score == 0:
        fitness = math.floor(0.5 * nbFrames * nbFrames)
    elif score < 10:
        fitness = math.floor(nbFrames * nbFrames) * math.pow(2,score) + 0.5
    else:
        fitness = math.floor(nbFrames * nbFrames) * math.pow(2,10) * (score-9) + 0.5
    return fitness

def playProces(individualList,resultList,height,width,queue):
    game = IAGame.Game(height, width)
    tmpResult = []
    for player in individualList:
        score = 0
        nbFrames = 0
        nbTurns = 0
        nextToWall = 0
        tmaxNotEat = 0
        tNotEat = 0
        finished = False
        while (not finished) and tNotEat < 100 and nbFrames < 5000:
            input = game.snake.lookAllDir(game.board)
            move = player.takeDecision(input)
            ch1 = ch2 = ch3 = ch4 = False
            if move == 0:
                ch1 = game.snake.changeDirection((0, 1))
            elif move == 1:
                ch2 = game.snake.changeDirection((0, -1))
            elif move == 2:
                ch3 = game.snake.changeDirection((1, 0))
            elif move == 3:
                ch4 = game.snake.changeDirection((-1, 0))
            game.snake.move()
            nbFrames += 1
            if game.snake.head()[0] >= game.board.height - 2 or game.snake.head()[0] <= 1 or game.snake.head()[
                1] >= game.board.width - 2 or game.snake.head()[1] <= 1:
                nextToWall += 1
            if ch1 or ch2 or ch3 or ch4:
                nbTurns += 1
            tNotEat += 1
            if (game.hasEaten()):
                game.snake.grow()
                game.board.createFruit()
                score += 1
                tmaxNotEat = max(tNotEat, tmaxNotEat)
                tNotEat = 0
            if game.end():
                finished = True
            if score == 0:
                tmaxNotEat = nbFrames
        fit = fitness([score, nbFrames, nbTurns, nextToWall, tmaxNotEat, tNotEat > 50])
        game.reset()
        tmpResult.append([fit,player])
    queue.put(tmpResult)

global next
class Genetics:
    def __init__(self,popsize,sizes):
        self.popSize = popsize
        self.population = [Network.Network(sizes) for i in range(0,self.popSize)]
        self.results = []
        self.bests = []
        self.genNum = 0
        self.average = 0
        self.maxFit = 0

    def bestOnes(self):
        nbWanted = 2
        bests = []
        def takeFirst(elem):
            return elem[0]
        for result in self.results:
            if len(bests)<0.5*self.popSize:
                bests.append(result)
            else:
                bests.sort(key=takeFirst,reverse=True)
                if result[0] > bests[-1][0]:
                    del bests[-1]
                    bests.append(result)
                    bests.sort(key=takeFirst,reverse=True)
        return bests

    def selectedForBreed(self):
        def takeFirst(elem):
            return elem[0]

        #self.results.sort(key=takeFirst, reverse=True)
        self.bests = []
        #self.bests.append(self.results[0])
        #random.shuffle(self.results)
        while len(self.bests) < 0.3*self.popSize:
            for result in self.results:
                chosen = (result[0] > random.uniform(-1,500))
                if chosen and len(self.bests) < 0.1*self.popSize and not result in self.bests:
                    self.bests.append(result)

    def createNewPop(self):
        tmp=[couple[1] for couple in self.bests]
        bestNeurons = [couple[1] for couple in self.bests]
        random.shuffle(bestNeurons)
        """while len(tmp) < self.popSize:
            breed = []
            while len(breed) < 2:
                for result in self.results:
                    chosen = (5 * result[0] > random.uniform(0,2 * self.maxFit))
                    if chosen and len(breed) < 2:
                        breed.append(result[1])
            children = breed[0].reproduction(breed[1])
            tmp.append(children[0])
            tmp.append(children[1])"""
        while len(tmp) < self.popSize:
            random.shuffle(bestNeurons)
            for par1,par2 in zip(bestNeurons[0::2],bestNeurons[1::2]):
                children = par1.reproduction(par2)
                tmp.append(children[0])
                tmp.append(children[1])
        self.population = tmp

    def mutation(self):
        for individual in self.population:
                individual.mutate()

    def playOneGen(self,height,width):
        self.maxFit = 0
        game = IAGame.Game(height,width)
        self.results = []
        self.average = 0
        queue1 = Queue()
        queue2 = Queue()
        queue3 = Queue()
        queue4 = Queue()
        queue5 = Queue()
        queue6 = Queue()
        queue7 = Queue()
        queue8 = Queue()
        queue9 = Queue()
        queue10 = Queue()
        list1 = [self.population[i] for i in range(0,self.popSize//10) ]
        list2 = [self.population[i] for i in range(self.popSize//10+1, 2* self.popSize // 10)]
        list3 = [self.population[i] for i in range(2* self.popSize//10 +1, 3* self.popSize//10)]
        list4 = [self.population[i] for i in range( 3* self.popSize//10 +1,  4* self.popSize//10)]
        list5 = [self.population[i] for i in range( 4* self.popSize//10 +1,  5* self.popSize//10)]
        list6 = [self.population[i] for i in range( 5* self.popSize//10 +1,  6* self.popSize//10)]
        list7 = [self.population[i] for i in range( 6* self.popSize//10 +1,  7* self.popSize//10)]
        list8 = [self.population[i] for i in range( 7* self.popSize//10 +1,  8* self.popSize//10)]
        list9 = [self.population[i] for i in range( 8* self.popSize//10 +1,  9* self.popSize//10)]
        list10 = [self.population[i] for i in range( 9* self.popSize//10 +1,   self.popSize-1)]

        process1 = Process(target=playProces, args=(list1, self.results ,height, width, queue1))
        process2 = Process(target=playProces, args=(list2, self.results, height, width, queue2))
        process3 = Process(target=playProces, args=(list3, self.results, height, width, queue3))
        process4 = Process(target=playProces, args=(list4, self.results, height, width, queue4))
        process5 = Process(target=playProces, args=(list4, self.results, height, width, queue5))
        process6 = Process(target=playProces, args=(list4, self.results, height, width, queue6))
        process7 = Process(target=playProces, args=(list4, self.results, height, width, queue7))
        process8 = Process(target=playProces, args=(list4, self.results, height, width, queue8))
        process9 = Process(target=playProces, args=(list4, self.results, height, width, queue9))
        process10 = Process(target=playProces, args=(list4, self.results, height, width, queue10))

        process1.start()
        process2.start()
        process3.start()
        process4.start()
        process5.start()
        process6.start()
        process7.start()
        process8.start()
        process9.start()
        process10.start()


        res = [queue1.get(),queue2.get(),queue3.get(),queue4.get(),queue5.get(),queue6.get(),queue7.get(),queue8.get(),queue9.get(),queue10.get()]
        process1.join()
        process2.join()
        process3.join()
        process4.join()
        process5.join()
        process6.join()
        process7.join()
        process8.join()
        process9.join()
        process10.join()
        for queue in res:
            for element in queue:
                self.results.append(element)
        for i in range(0,len(self.results)):
            self.average += self.results[i][0]
        self.average/=len(self.results)
        self.genNum+=1




#Definition of some functions cause I need em
def moyenne(liste):
    av = 0
    for element in liste:
        av += element
    av /= len(liste)
    return av

def variance(liste):
    av = moyenne(liste)
    partSum = 0
    for element in liste:
        partSum += math.pow(element-av,2)
    variance = partSum / len(liste)
    return variance

def normalize(liste):
    tmp = []
    av = moyenne(liste)
    var = variance(liste)
    for element in liste:
        tmpelement = (element - av) / var
        tmp.append(tmpelement)
    return tmp


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
    gen = Genetics(GenerationSize,[24,15,4])
    print(nbGenerationToRun)
    fitlognum = len([name for name in os.listdir('fit')])
    os.system('rm -rf Logs')
    os.system('mkdir Logs')
    for i in range(0,nbGenerationToRun):
        if i % 10 ==0:
            os.system('mkdir Logs/Generation{}'.format(i))
    os.system('mkdir Logs/Generation{}'.format(nbGenerationToRun-1))
    for i in range(0,nbGenerationToRun):
        print("Generation numero: {}".format(i))
        gen.playOneGen(height,width)
        #gen.selectedForBreed()
        #gen.bests = []
        gen.bests = gen.bestOnes()
        gen.createNewPop()
        gen.mutation()
        print("Pop: {}".format(len(gen.population)))
        average = 0
        for result in gen.bests:
            average+=result[0]
            if i % 10 ==0 or i==nbGenerationToRun-1:
                with open('Logs/Generation{}/result.log'.format(gen.genNum-1), 'w') as file:
                    average = 0
                    for result in gen.bests:
                        average+=result[0]
                        file.write('Fitness: {}\n'.format(result[0]))
                    file.write("Average fitness: {} \n".format(gen.average))
        fit.append(gen.average)
    #fit = normalize(fit)
    with open('fit/fitresult{}.csv'.format(fitlognum),'w') as file:
        for element in fit:
            file.write("{}\n".format(element))
    gen.bests = gen.bestOnes()
    for best in gen.bests:
        bestEver.append(best)
    os.system('mkdir GenNeurLog')
    neurIndex = 0
    for neuron in gen.bests:
        with open('GenNeurLog/Neuron{}'.format(neurIndex),'w') as logfile:
            logfile.write(neuron[1].tolog())
        neurIndex+=1
    global next
    next = False
    sys.stdout.write('\a')
    sys.stdout.flush()
    a = input("Enter to play last gen")
    with keyboard.Listener(on_press=on_press) as listener:
        for element in bestEver:
            network = element[1]
            game = IAGame.Game(height,width)
            game.printG()
            finished = False;
            score = 0;
            tNotEat = 0
            while not finished and tNotEat <100:
                time.sleep(0.05)
                inp = game.snake.lookAllDir(game.board)
                move = network.takeDecision(inp)
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
                    tNotEat -= 50
                if game.end():
                    finished = True
                os.system('clear')
                tNotEat +=1
                game.printG()
                next = False
                print(score)
            b=input("Continuer")
            os.system('clear')