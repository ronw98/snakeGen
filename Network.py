import random
import math
class Network:
    def __init__(self,sizes,zero=False):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        if zero == False:
            self.num_layers = 3
            self.sizes = sizes
            self.biases = [[random.uniform(-1,1) for x in range(0,y)] for y in sizes[1:]]
            self.weights = [[[random.uniform(-1,1) for prevneuron in range(0,sizes[i-1])]for neuron in range(0,sizes[i])]
                            for i in range(1,3)]
        else:
            self.num_layers = 3
            self.sizes = sizes
            self.biases = [[0 for x in range(0,y)] for y in sizes[1:]]
            self.weights = [[[0 for prevneuron in range(0,sizes[i-1])]for neuron in range(0,sizes[i])]
                            for i in range(1,3)]


    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        outputValues = []
        hidValues = []
        #hidden layer values
        #for each neuron
        for neuron in range(0,self.sizes[1]):
            #compute linear combination
            z = 0
            for weight in range(0,self.sizes[0]):
                z+= a[weight] * self.weights[0][neuron][weight]
            z+= self.biases[0][neuron]
            z=sigmoid(z)
            hidValues.append(z)
        #output values
        for neuron in range(0,self.sizes[2]):
            z = 0
            for weight in range(0,self.sizes[1]):
                z+= hidValues[weight] * self.weights[1][neuron][weight]
            z+= self.biases[1][neuron]
            z = sigmoid(z)
            outputValues.append(z)
        return outputValues

    def takeDecision(self,input):
        return findMax(self.feedforward(input))

    def reproduction(self,network):
        child1 = Network(self.sizes)
        child2 = Network(self.sizes)
        for k in range(1,len(self.sizes)):
            cut1 = random.randint(0,self.sizes[k]*self.sizes[k-1]-1)
            cut2 = cut1 + random.randint(0,self.sizes[k]*self.sizes[k-1]-1-cut1)
            cutI1 = cut1 // self.sizes[k-1]
            cutJ1 = cut1 - cutI1*self.sizes[k-1]
            cutI2 = cut2 // self.sizes[k - 1]
            cutJ2 = cut2 - cutI2 * self.sizes[k - 1]
            #For neurons before cut neuron, we simply copy the values from par1
            for i in range(0,cutI1):
                for j in range(0,self.sizes[k-1]):
                    child1.weights[k-1][i][j] = self.weights[k-1][i][j]
                    child2.weights[k-1][i][j] = network.weights[k-1][i][j]

                child1.biases[k-1][i] = self.biases[k - 1][i]
                child2.biases[k-1][i] = network.biases[k-1][i]
            #For the cut neuron, we copy one part from par1 and one part from par2
            for j in range(0, cutJ1):
                child1.weights[k - 1][cutI1][j] = self.weights[k - 1][cutI1][j]
                child2.weights[k - 1][cutI1][j] = network.weights[k - 1][cutI1][j]
            for j in range(cutJ1, self.sizes[k - 1]):
                child2.weights[k - 1][cutI1][j] = self.weights[k - 1][cutI1][j]
                child1.weights[k - 1][cutI1][j] = network.weights[k - 1][cutI1][j]
            #Second cut until cut neuron
            for i in range(cutI1+1,cutI2):
                for j in range(0, self.sizes[k-1]):
                    child2.weights[k - 1][i][j] = self.weights[k - 1][i][j]
                    child1.weights[k - 1][i][j] = network.weights[k - 1][i][j]
                child2.biases[k - 1][i] = self.biases[k - 1][i]
                child1.biases[k - 1][i] = network.biases[k - 1][i]
            #Cut neuron
            for j in range(0, cutJ2):
                child2.weights[k - 1][cutI2][j] = self.weights[k - 1][cutI2][j]
                child1.weights[k - 1][cutI2][j] = network.weights[k - 1][cutI2][j]
            for j in range(cutJ2, self.sizes[k - 1]):
                child1.weights[k - 1][cutI2][j] = self.weights[k - 1][cutI2][j]
                child2.weights[k - 1][cutI2][j] = network.weights[k - 1][cutI2][j]

            #For neurons after second cut neuron, we copy the values from par2
            for i in range(cutI2+1,self.sizes[k]):
                for j in range(0, self.sizes[k-1]):
                    child1.weights[k-1][i][j] = self.weights[k-1][i][j]
                    child2.weights[k-1][i][j] = network.weights[k-1][i][j]
                child1.biases[k-1][i] = self.biases[k-1][i]
                child2.biases[k-1][i] = network.biases[k-1][i]
        return [child1,child2]

    def mutate(self):
        for layer in self.weights:
            for neuron in layer:
                    for weight in neuron:
                        i = random.uniform(0,1000)
                        if i == 0:
                            weight+= random.randint(-1,1) * random.uniform(0,0.75)
                            if weight > 1:
                                weight =1
                            if weight < -1:
                                weight = -1
        for layer in self.biases:
            for bias in layer:
                i = random.randint(0,1000)
                if i == 0:
                    bias += random.randint(-1,1) * random.uniform(0,0.75)
                    if bias > 1:
                        bias = 1
                    if bias < -1:
                        bias = -1
    def tolog(self):
        result = ""
        for layer in self.weights:
            for neuron in layer:
                for weight in neuron:
                    result +="{} ".format(weight)
                result+="\n"
            result+="\n\n"
        result+="\n\n\n"
        for layer in self.biases:
            for neuronBias in layer:
                result+="{}".format(neuronBias)
                result+="\n"
            result+="\n\n"


def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+math.exp(-z))

def relu(z):
    if z < 0:
        return 0
    return z

def findMax(tab):
    imax = 0
    max = tab[0]
    for i in range(1,len(tab)):
        if tab[i]>max:
          imax=i
          max = tab[i]
    return imax

if __name__  ==  '__main__':
    net1 =Network([2,5,3])
    net2 = Network([2,5,3])
    children = net1.reproduction(net2)
