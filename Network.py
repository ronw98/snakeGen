import random
import math
class Network:
    def __init__(self):
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
        self.num_layers = 3
        sizes = [2400,20,4]
        self.sizes = sizes
        self.biases = [[random.uniform(-10,10) for x in range(0,y)] for y in sizes[1:]]
        print(self.biases[1])
        self.weights = [[[random.uniform(-1,1) for prevneuron in range(0,sizes[i-1])]for neuron in range(0,sizes[i])]
                        for i in range(1,3)]
        print(len(self.weights[0][1]))

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""
        outputValues = []
        hidValues = []
        #hidden layer values
        #for each neuron
        for neuron in range(0,20):
            #compute linear combination
            z = 0
            for weight in range(0,2400):
                z+= a[weight] * self.weights[0][neuron][weight]
            z+= self.biases[0][neuron]
            z=sigmoid(z)
            hidValues.append(z)
        #output values
        for neuron in range(0,4):
            z = 0
            for weight in range(0,20):
                z+= hidValues[weight] * self.weights[1][neuron][weight]
            z+= self.biases[1][neuron]
            z = sigmoid(z)
            outputValues.append(z)
        print(outputValues)
        return outputValues

    def takeDecision(self,input):
        return findMax(self.feedforward(input))

def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+math.exp(-z))
def findMax(tab):
    imax = 0
    max = tab[0]
    for i in range(1,len(tab)):
        if tab[i]>max:
          imax=i
          max = tab[i]
    return imax

if __name__  ==  '__main__':
    print(findMax([1,2,3,4]))