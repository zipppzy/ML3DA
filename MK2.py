import math
from abc import ABC, abstractmethod

class Neuron:
    def __init__(self,numInputs,activationFunc,sigmoidConstant=1,stepLimit=0):
        self.activationFunc=activationFunc
        self.numInputs=numInputs
        self.weights=[]
        self.sigmoidConstant=sigmoidConstant
        self.stepLimit=stepLimit
    def setWeights(self,weights):
        if(len(weights)==self.numInputs):
            self.weights=weights
    def setActivationFunc(self,activationFunc):
        self.activationFunc=activationFunc
    def setSigmoidConstant(self,sigmoidConstant):
        self.sigmoidConstant=sigmoidConstant
    def setStepLimit(self,stepLimit):
        self.stepLimit=stepLimit
    def getOutput(self,inputs):
        if(len(inputs)==self.numInputs and len(self.weights)>0):
            activation=0
            for i in range(self.numInputs):
                activation+=inputs[i]*self.weights[i]
            if(self.activationFunc=="sum"):
                return activation
            if(self.activationFunc=="sigmoid"):
                return 1/(1+(math.e**((activation*-1)/self.sigmoidConstant)))
            if(self.activationFunc=="step"):
                if (activation>=self.stepLimit):
                    return 1
                else: return 0

class Layer:
    def __init__(self,numNeurons,numInputs,activationFunc,sigmoidConstant=1,stepLimit=0):
        #mabeye remove later
        self.numInputs=numInputs
        self.layer=[]
        for i in range(numNeurons):
            self.layer.append(Neuron(numInputs,activationFunc,sigmoidConstant,stepLimit))

    def setWeights(self,weights):
        if (len(weights)==len(self.layer)):
            for i in range(len(self.layer)):
                if(len(weights[i])==self.layer[i].numInputs):
                    self.layer[i].setWeights(weights[i])

    def setActivationFunc(self,activationFunc):
        for i in self.layer:
            i.setActivationFunc(activationFunc)

    def setSigmoidConstant(self,sigmoidConstant):
        for i in self.layer:
            i.setSigmoidConstant(sigmoidConstant)

    def setStepLimit(self,stepLimit):
        for i in self.layer:
            i.setStepLimit(stepLimit)

    def getOutput(self,inputs):
        if(len(inputs)==self.numInputs):
            output=[]
            for i in self.layer:
                output.append(i.getOutput(inputs))
        return output

class NeuralNet:
    def __init__(self,structure,numInputs,activationFunc,sigmoidConstant=1,stepLimit=0):
        self.numInputs=numInputs
        self.neuralNet=[]
        self.neuralNet.append(Layer(structure[0],numInputs,activationFunc,sigmoidConstant,stepLimit))
        for i in range(1,len(structure)):
            self.neuralNet.append(Layer(structure[i],structure[i-1],activationFunc,sigmoidConstant,stepLimit))
    #put check on this        
    def setWeights(self,weights):
        for i in range(len(self.neuralNet)):
            self.neuralNet[i].setWeights(weights[i])
                   

    def setActivationFunc(activationFunc):
        for i in self.neuralNet:
            i.setActivationFunc(activationFunc)
    def setSigmoidConstant(sigmoidConstant):
        for i in self.neuralNet:
            i.setsigmoidConstant(sigmoidConstant)
    def setStepLimit(self,stepLimit):
        for i in self.neuralNet:
            i.setStepLimit(stepLimit)
    def getOutput(self,inputs):
        if (len(inputs)==self.numInputs):
            tempIn=inputs
            for i in range(len(self.neuralNet)):
                tempIn=self.neuralNet[i].getOutput(tempIn)
            return tempIn

#n=NeuralNet([3,3],1,"sum")
#n.setWeights([[[1],[1],[1]],[[1,1,1],[1,1,1],[1,1,1]]])
#print(n.getOutput([1]))



