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
import math
import time
from multiprocessing import Process, Lock, Queue

lock = Lock()


# The main class for the genetic algorithm
class Genetics:
    def __init__(self,popsize,sizes,directory=None):
        self.popSize = popsize
        if directory is None:
            self.population = [Network.Network(sizes) for i in range(0,self.popSize)]
        else:
            filelist = os.listdir(directory)
            self.population = [Network.fromLog(directory+file,sizes) for file in filelist]
        self.results = []
        self.bests = []
        self.genNum = 0
        self.average = 0
        self.maxFit = 0

    # Returns a list containing the best elements of the generation, along with their fitness (but not in that order)
    def bestOnes(self):
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

    # Creates a new population from the last one
    def createNewPop(self):
        # Fills half of the new population with the best elements of the old one
        tmp = [couple[1] for couple in self.bests]

        # Creates the list of parents to the next generation
        bestNeurons = [couple[1] for couple in self.bests]
        random.shuffle(bestNeurons)

        # Breeds individuals until desired size is reached
        while len(tmp) < self.popSize:
            random.shuffle(bestNeurons)
            for par1,par2 in zip(bestNeurons[0::2],bestNeurons[1::2]):
                children = par1.reproduction(par2)
                tmp.append(children[0])
                tmp.append(children[1])
        self.population = tmp

    # Mutates the population
    def mutation(self):
        for individual in self.population:
                individual.mutate()

    # Plays one generation of individuals
    def playOneGen(self,height,width):
        self.maxFit = 0
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

        process1 = Process(target=playProces, args=(list1, height, width, queue1))
        process2 = Process(target=playProces, args=(list2, height, width, queue2))
        process3 = Process(target=playProces, args=(list3, height, width, queue3))
        process4 = Process(target=playProces, args=(list4, height, width, queue4))
        process5 = Process(target=playProces, args=(list5, height, width, queue5))
        process6 = Process(target=playProces, args=(list6, height, width, queue6))
        process7 = Process(target=playProces, args=(list7, height, width, queue7))
        process8 = Process(target=playProces, args=(list8, height, width, queue8))
        process9 = Process(target=playProces, args=(list9, height, width, queue9))
        process10 = Process(target=playProces, args=(list10, height, width, queue10))


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
            for individual in queue:
                self.results.append(individual)
        for j in range(0,len(self.results)):
            self.average += self.results[j][0]
        self.average/=len(self.results)
        self.genNum+=1


# Returns the computed fitness from the game results
def fitness(gameRes):
    score = gameRes[0]
    nbFrames = gameRes[1]
    if score == 0:
        fitnessRes = math.floor(0.5 * nbFrames * nbFrames)
    elif score < 10:
        fitnessRes = math.floor(nbFrames * nbFrames) * math.pow(2,score) + score/100
    else:
        fitnessRes = math.floor(nbFrames * nbFrames) * math.pow(2,10) * (score-9) + score/100
    return fitnessRes

# Defines the action of a process, which is to let the individual in the list play snake
def playProces(individualList, gameHeight, gameWidth, queue):
    gameSession = IAGame.Game(gameHeight, gameWidth)
    tmpResult = []
    for player in individualList:
        fit = fitness(gameSession.play(player))
        tmpResult.append([fit, player])
        gameSession.reset()
    queue.put(tmpResult)


# Creates and returns the help test
def createHelp():
    help = 'This programm is a genetic algorithm trying to play snake\n'
    help += 'python3 Genetics.py [option] <argument>\n'
    help += 'List of options:\n'
    help += ' --help : show this window\n'
    help += '    -n : number of generations to train on\n'
    help += '    -s : number of individuals in a generation\n'
    help += '    -h : height of the board\n'
    help += '    -w : width of the board\n'
    help += '    -f : folder from which recreating a population'
    help += 'Example: python3 Genetics.py -n 10 -s 100'
    return help

if __name__=='__main__':
    """ Initializes the default parameters """
    nbGenerationToRun = 2
    GenerationSize = 20
    height = 30
    width = 30
    sourceFolder = None
    """ Checks all the arguments given"""
    for i in range(1, len(sys.argv),2):
        opt = sys.argv[i]
        if opt == '--help':
            print(createHelp())
            exit(-12)
        elif opt == '-h':
            height = int(sys.argv[i+1])
        elif opt == '-w':
            width = int(sys.argv[i+1])
        elif opt == '-n':
            nbGenerationToRun = int(sys.argv[i+1])
        elif opt == '-s':
            GenerationSize = int(sys.argv[i+1])
        elif opt == '-f':
            sourceFolder = sys.argv[i+1]
        else:
            print('Ntm ça marche pas, type --help for more details\n')
            sys.exit()

    # Genetic creation
    gen = Genetics(GenerationSize,[24,15,4], sourceFolder)

    # Initializes the fitness history
    fitnessHistory = []
    # Initializes bests history
    bestEver = []

    print("The program will run {} generations".format(nbGenerationToRun))

    # Determines the name to give to the fitness.csv file
    fitlognum = len([name for name in os.listdir('fit')])

    # Cleans the Logs folder and re-generates it
    os.system('rm -rf Logs')
    os.system('mkdir Logs')
    for i in range(0,nbGenerationToRun):
        if i % 10 ==0:
            os.system('mkdir Logs/Generation{}'.format(i))
    os.system('mkdir Logs/Generation{}'.format(nbGenerationToRun-1))

    # Plays the number of generations asked
    for i in range(0,nbGenerationToRun):
        # Determines the time necessary to play one generation
        start = time.time()
        print("Generation numero: {} / {}".format(i,nbGenerationToRun))

        gen.playOneGen(height,width)
        # Sets the bests individuals of the generation
        gen.bests = gen.bestOnes()
        gen.createNewPop()
        gen.mutation()

        # Computes various things for logs: computes the average result of the best ones, and the result for each best individual
        if i % 10 ==0 or i==nbGenerationToRun-1:
            with open('Logs/Generation{}/result.log'.format(gen.genNum-1), 'w') as file:
                average = 0
                for result in gen.bests:
                    average+=result[0]
                    file.write('Fitness: {}\n'.format(result[0]))
                file.write("Average fitness: {} \n".format(gen.average))
        fitnessHistory.append(gen.average)

        # Print the time elapsed to play the generation
        print("Elapsed time: ", time.time()-start)

    # At the end of all generations, prints the fitness history into the right file
    with open('fit/fitresult{}.csv'.format(fitlognum),'w') as file:
        for element in fitnessHistory:
            file.write("{}\n".format(element))

    # Saves the best individuals of the last generation on the disk
    os.system('mkdir GenNeurLog')
    neurIndex = 0
    for neuron in gen.bests:
        with open('GenNeurLog/Neuron{}'.format(neurIndex),'w') as logfile:
            logfile.write(neuron[1].tolog())
        neurIndex+=1

    # Makes a sound when everything is done and the user can see the results
    sys.stdout.write('\a')
    sys.stdout.flush()

    a = input("Enter to play last gen")

    # Plays the best individuals of last gen, with graphic feedback
    game = IAGame.Game(height,width)
    for element in gen.bests:
        game.play(element[1],True,0.05)
        b=input("Continuer")
        os.system('clear')
