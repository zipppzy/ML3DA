import math
from abc import ABC, abstractmethod
import random

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


class GenAlg(ABC):
	def __init__(self,numGens,numIndivs,crossoverRate,mutationRate,culledPercent,structure,numInputs,activationFunc,sigmoidConstant=1,stepLimit=0):
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

	#quite broken
##	def randomWeights(self):
##		#makes a list for each layer
##		weights=[[0]*len(self.structure)]
##		#makes a list for each neuron
##		for i in range(len(weights)):
##			weights[i][0]=[]for j in range(self.structure[i])
##                        for j in range(len(weights[i])):
                                
                                

##g=GenAlg(1,2,.1,.1,.1,[2,3],1,"sigmoid")
##for i in g.gen:
##	print(g.getWeights())
a=[[]for i in range(5)]
for i in range(len(a)):
        for i in range
        a[i].append([0])
print(a)

