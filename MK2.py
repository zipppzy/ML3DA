#goal is to make all classes take inputs after instantiation
import random
import math
import unittest
from operator import attrgetter
class Neuron:
	def __init__(self,inputs):
		#make the weights
		self.weights=[]
		for i in inputs:
			self.weights.append((random.random()*2)-1)
		#activation function
		#multiply the inputs and weights and sum them
		self.sum=0.0
		for x in range(len(inputs)-1):
			self.sum+=inputs[x]*self.weights[x]
		self.activation=self.sum
		def setWeights(self,weights):
			self.inputWeights=weights
class Layer:
	def __init__(self,i,nN):
		self.layerArr=[]
		self.numNeuron=nN
		for x in range(nN):
			#make more generalized
			self.layerArr.append(Neuron(i))
	def getOutput(self):
		output=[]
		for i in range(len(self.layerArr)):
			output.append(self.layerArr[i].activation)
		return output
	def getWeights(self):
		weights=[]
		for i in range(len(self.layerArr)):
			weights.append(self.layerArr[i].weights)
		return weights
	def setWeights(self,w):
		for i in range(len(self.layerArr)):
			self.layerArr[i].setWeights=w[i]


class NeuralNet:

	#netStructArr is a a array with number of layers and number of nuerons per layer
	def __init__(self,inputs,netStructArr):
		global point1
		global point2
		self.neuralNet=[]
		self.inputs=inputs
		#making first layer with initial inputs; random weights
		self.neuralNet.append(Layer(self.inputs,netStructArr[0]))
		#make the rest of the layers using the output of the first
		for i in range(1,len(netStructArr)):
			self.neuralNet.append(Layer(self.neuralNet[i-1].getOutput(),netStructArr[i]))
		self.output=self.neuralNet[len(self.neuralNet)-1].getOutput()
		#fitness function is distance from point 2 after moving
		self.fitness=test(self)
		self.weights=[]
		for i in self.neuralNet:
			self.weights.append(i.getWeights())

	def setInputs(self,inputs){
		weights=getWeights()
		self.inputs=inputs
		self.neuralNet=[]
		self.neuralNet.append(Layer(self.inputs,netStructArr[0]))
		#make the rest of the layers using the output of the first
		for i in range(1,len(netStructArr)):
			self.neuralNet.append(Layer(self.neuralNet[i-1].getOutput(),netStructArr[i]))
		self.output=self.neuralNet[len(self.neuralNet)-1].getOutput()
	}
	def setWeights(self,w):
		for i in range(len(self.neuralNet)):
			self.neuralNet[i].setWeights(w[i])
	def getWeights(self){
		weights=[]
		for i in self.neuralNet:
			self.weights.append(i.getWeights)
	}
		

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y
		# returns a vector between two points with distance then angle  
	def vector(self,a):
		v=[]
		v.append(math.sqrt(((a.x-self.x)**2)+((a.y-self.y)**2)))
		v.append(math.atan2(a.x-self.x,a.y-self.y))
		return v		
def generate(numInd,netStruct):
	global inputs
	generation=[]
	for i in range(numInd):
		generation.append(NeuralNet(inputs,netStruct))
	return generation
def cullTheWeak(gen,surviorNum):
	culledGen=sorted(gen,key=attrgetter('fitness'))
	culledGen=culledGen[:surviorNum]
	culledGen.reverse()
	return culledGen

#return 4 weights for neural Nets
def reproduce(neuralNet1,neuralNet2):
	randVal=math.floor(random.random()*(len(neuralNet1.getWeights())))
	piece1=neuralNet1.getWeights()[:randVal]
	piece2=neuralNet1.getWeights()[randVal:len(neuralNet1.getWeights())]
	piece3=neuralNet2.getWeights()[:randVal]
	piece4=neuralNet2.getWeights()[randVal:len(neuralNet1.getWeights())]
	return [piece1+piece4,piece2+piece3]

# def test(NeuralNet a):
# 	global maxDistance
# 	target=Point(math.floor(random.random()*100),math.floor(random.random()*100))
# 	player=Point(math.floor(random.random()*100),math.floor(random.random()*100))
# 	while(player.vector(target)[0]>maxDistance):







#-----CONSTANTS-------
#instatiate 2 points and a vector between them as input
point1=Point(4,2)
point2=Point(20,50)
inputs=point1.vector(point2)
structure=[10,7,2]
genSize=7
maxGens=100
culledGenSize=2
done=False
j=0
maxDistance=2
gen1=generate(genSize,structure)
while(done==False and j<maxGens):
	j=j+1
	gen1=cullTheWeak(gen1,culledGenSize)
	
	if(gen1[0].fitness>.05):
		done=True
		break;
	print(gen1[0].fitness)
	while(len(gen1)<genSize):
		#print(str(len(gen1))+"\t"+str(j))
		randVal1=math.floor(random.random()*culledGenSize)
		randVal2=math.floor(random.random()*culledGenSize)
		while(randVal2==randVal1):
			randVal2=math.floor(random.random()*culledGenSize)
		childrenWeights=reproduce(gen1[randVal1],gen1[randVal2])
		child1=NeuralNet(inputs,structure)
		child1.setWeights(childrenWeights[0])
		child2=NeuralNet(inputs,structure)
		child2.setWeights(childrenWeights[1])
		gen1.append(child1)
		gen1.append(child2)
	if(len(gen1)>genSize):
		gen1.pop(len(gen1)-1)

print(gen1[0].fitness)



