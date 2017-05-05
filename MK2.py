import math
import abc
import random
import operator

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
        def getWeights(self):
                weights=[]
                for i in self.layer:
                        weights.append(i.weights)
                return weights

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
                self.fitness=0
                for i in range(1,len(structure)):
                        self.neuralNet.append(Layer(structure[i],structure[i-1],activationFunc,sigmoidConstant,stepLimit))
        #put check on this        
        def setWeights(self,weights):
                for i in range(len(self.neuralNet)):
                        self.neuralNet[i].setWeights(weights[i])
        def getWeights(self):
                weights=[]
                for i in self.neuralNet:
                        weights.append(i.getWeights())
                return weights
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


class GenAlg():
        __metaclass__=abc.ABCMeta
        
        def __init__(self,numGens,numIndivs,crossoverRate,mutationRate,culledPercent,structure,numInputs,activationFunc,sigmoidConstant=1,stepLimit=0): #10
                # GenAlg(1,2,.1,.1,.1,[2,3],1,"sigmoid")
                self.numGens=numGens
                self.numIndivs=numIndivs
                self.crossoverRate=crossoverRate
                self.mutationRate=mutationRate
                self.culledPercent=culledPercent
                self.structure=structure
                self.numInputs=numInputs
                #self.sigmoidConstant=sigmoidConstant
                #self.stepLimit=stepLimit
                self.gen=[]
                for i in range(numIndivs):
                        self.gen.append(NeuralNet(structure,numInputs,activationFunc,sigmoidConstant,stepLimit))
                for i in self.gen:
                        i.setWeights(self.randomWeights())
                

        def randomWeights(self):
                weights=[]
                for i in range(len(self.structure)):
                        weights.append([])
                for i in range(len(self.structure)):
                        for j in range(self.structure[i]):
                                weights[i].append(self.randomNeuronWeights(i))
                return weights

        def randomNeuronWeights(self,layerNum):
                weights=[]
                if (layerNum==0):
                        for i in range(self.numInputs):
                                weights.append(random.random())
                elif(layerNum>0):
                        for i in range (self.structure[layerNum-1]):
                                weights.append(random.random())
                return weights         
        @abc.abstractmethod
        def fitnessFunction(self):
                pass
        def cull(self):
                self.gen.sort(key=operator.attrgetter("fitness"),reverse=True)
                self.gen=self.gen[1:int(len(self.gen)*self.culledPercent)]
        #def reproduce(self):
                
        def crossover(self):
        

        def 3Dto1D(3D):
                1D=[]
                for i in 3D:
                        for j in i:
                                for k in j:
                                        1D.append(k)
                return b
        def 1Dto3D(self,1D):
                1DCounter=0
                3D=[]
                for i in range(len(self.structure)):
                        3D.append([])
                for i in range(len(self.structure)):
                        
                        for j in range(self.structure[i]):
                                
                                neuronWeights=[]
                                if (i==0):
                                        for i in range(self.numInputs):
                                                neuronWeights.append(1D[1DCounter])
                                                1DCounter++
                                                
                                elif(i>0):
                                        for i in range (self.structure[i-1]):
                                                neuronWeights.append(1D[1DCounter])
                                                1DCounter++
                                3D[i].append(neuronWeights)                
                                
                                
g=GenAlg(1,10,.1,.1,.1,[2,3],1,"sigmoid")
g.cull()

for i in g.gen:
        print(i.fitness)


                




