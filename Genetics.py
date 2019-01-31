import Network
import IAGame

class Genetics:
    def __init__(self):
        self.popSize = 200
        self.population = [Network() for i in range(0,self.popSize)]
        self.results = []

    def fitness(self,gameRes):
        score = gameRes[0]
        nbFrames = gameRes[1]
        return 10*score + nbFrames

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