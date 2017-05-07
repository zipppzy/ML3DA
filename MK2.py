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
                self.sigmoidConstant=sigmoidConstant
                self.stepLimit=stepLimit
                self.gen=[]
                for i in range(numIndivs):
                        self.gen.append(NeuralNet(structure,numInputs,activationFunc,sigmoidConstant,stepLimit))
                for i in self.gen:
                        i.setWeights(self.randomWeights())
                for i in range(numGens):
                	self.cull()
                	self.reproduce()

                

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
        def reproduce(self):
        	culledNum=len(self.gen)
        	while(len(self.gen)<self.numIndivs):
        		choice1=int(random.random()*culledNum)
        		choice2=int(random.random()*culledNum)
        		while(choice2==choice1):
        			choice2=int(random.random()*culledNum)
        		children=self.crossover(self.gen[choice1].getWeights(),gen[choice2].getWeights())
        		self.gen.append(NeuralNet(self.structure,self.numInputs,self.activationFunc,self.sigmoidConstant,self.stepLimit))
        		self.gen[len(self.gen)-1].setWeights(children[0])
        		self.gen.append(NeuralNet(self.structure,self.numInputs,self.activationFunc,self.sigmoidConstant,self.stepLimit))
        		self.gen[len(self.gen)-1].setWeights(children[1])
        	if(len(self.gen)>self.numIndivs):
        		del self.gen[len(self.gen)-1]
                
        def crossover(self,A,B):
        	weightsA=self.threeDtoOneD(A)
        	weightsB=threeDtoOneD(B)
        	cutPoint=int(random.random()*(len(weightsA)-1))+1
        	piece1A=weightsA[0:cutPoint]
        	piece2A=weightsA[cutPoint:len(weightsA)]
        	piece1B=weightsB[0:cutPoint]
        	piece2B=weightsB[cutPoint:len(weightsB)]
        	child1=piece1A+piece2B
        	child2=peice1B+piece2A
        	for i in child1:
        		if(random.random()<self.mutationRate):
        			i=random.random()
        	child2=peice1B+piece2A
        	for i in child2:
        		if(random.random()<self.mutationRate):
        			i=random.random()
        	child1=oneDtoThreeD(child1)
        	child2=oneDtoThreeD(child2)
        	return [child1,child2]



        

        def threeDtoOneD(self,three):
                one=[]
                for i in three:
                        for j in i:
                                for k in j:
                                        one.append(k)
                return b
        def oneDtoThreeD(self,one):
                oneCounter=0
                three=[]
                for i in range(len(self.structure)):
                        three.append([])
                for i in range(len(self.structure)):
                        
                        for j in range(self.structure[i]):
                                
                                neuronWeights=[]
                                if (i==0):
                                        for i in range(self.numInputs):
                                                neuronWeights.append(one[oneCounter])
                                                oneCounter+=1
                                                
                                elif(i>0):
                                        for i in range (self.structure[i-1]):
                                                neuronWeights.append(one[oneCounter])
                                                oneCounter+=1
                                three[i].append(neuronWeights)
                return three                               
                        
g=GenAlg(1,10,.1,.2,.1,[2,3],1,"sigmoid")


for i in g.gen:
        print(i.fitness)


                




