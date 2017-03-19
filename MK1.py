#goal is to make all classes take inputs after instantiation
import random
import math
import unittest
import turtle
import time
from operator import attrgetter
#represents one neuron in a neural network
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
#represents multiple neurons
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

#represents multiple layers. Is tested to get fitness
class NeuralNet:

	#netStructArr is a a array with number of layers and number of nuerons per layer
	def __init__(self,inputs,netStructArr):
		global point1
		global point2
		self.neuralNet=[]
		self.inputs=inputs
		self.neuralNet.append(Layer(self.inputs,netStructArr[0]))
		for i in range(1,len(netStructArr)):
			self.neuralNet.append(Layer(self.neuralNet[i-1].getOutput(),netStructArr[i]))
		self.output=self.neuralNet[len(self.neuralNet)-1].getOutput()
		#fitness function is distance from point 2 after moving
		testPoint=Point(point1.x+self.output[0],point1.y+self.output[1])
		self.fitness=testPoint.vector(point2)[0]
		self.weights=[]
		for i in self.neuralNet:
			self.weights.append(i.getWeights())

	
	def setWeights(self,w):
		#resolve problems here
		for i in range(len(self.neuralNet)):
			self.neuralNet[i]=w[i]
		#for i in self.neuralNet:
		#	i.setWeights(w)
	
		
#a point with x and y coordinates
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
#creates an array of NeuralNets
def generate(numInd,netStruct):
	global inputs
	generation=[]
	for i in range(numInd):
		generation.append(NeuralNet(inputs,netStruct))
	return generation
#sorts a generation on the basis of fitness
def cullTheWeak(gen,surviorNum):
	culledGen=sorted(gen,key=attrgetter('fitness'))
	culledGen=culledGen[:surviorNum]
	
	return culledGen

#return 4 weights for neural Nets
#right now is broken
def reproduce(neuralNet1,neuralNet2):
	randVal=math.floor(random.random()*(len(neuralNet1.weights)))
	piece1=neuralNet1.weights[:randVal]
	piece2=neuralNet1.weights[randVal:len(neuralNet1.weights)]
	piece3=neuralNet2.weights[:randVal]
	piece4=neuralNet2.weights[randVal:len(neuralNet1.weights)]
	return [piece1+piece4,piece2+piece3]
#turtle stuff that will be removed later so wont bother to explain it
def reset():
	global turnt
	turnt.reset()
	turnt.speed(10)
	turnt.pensize(8)
	turnt.penup()
	turnt.goto(point1.x,point1.y)
	turnt.dot(15,"green")
	turnt.goto(point2.x,point2.y)
	turnt.dot(15,"red")
	turnt.goto(point1.x,point1.y)
	turnt.pendown()
# def test(NeuralNet a):
# 	global maxDistance
# 	target=Point(math.floor(random.random()*100),math.floor(random.random()*100))
# 	player=Point(math.floor(random.random()*100),math.floor(random.random()*100))
# 	while(player.vector(target)[0]>maxDistance):







#-----CONSTANTS-------
#instatiate 2 points and a vector between them as input
point1=Point(4,2)
point2=Point(100,127)
inputs=point1.vector(point2)
#this indicates how many layers and how many neruons are in each layer in the neural network
structure=[15,20,2]
#how large the unculled generation is
genSize=100
#how many generations to go before stopping
maxGens=100
#how many individuals to keep after culling
culledGenSize=5
#just ways to end the loop
done=False
j=0
#max distance from point 2 that can be called a sucess
maxDistance=2

#----Setting up turtle-----
window=turtle.Screen()
turnt=turtle.Turtle()
turnt.speed(10)
turnt.pensize(8)
turnt.penup()
turnt.shape("blank")
turnt.goto(point1.x,point1.y)
turnt.dot(15,"green")
turnt.goto(point2.x,point2.y)
turnt.dot(15,"red")
turnt.goto(point1.x,point1.y)
turnt.pendown()

#should put this all in a method at some point
gen1=generate(genSize,structure)
while(done==False and j<maxGens):
	j=j+1
	gen1=cullTheWeak(gen1,culledGenSize)
	#turtle stuff
	turnt.forward(gen1[0].output[0])
	turnt.left(90)
	turnt.forward(gen1[0].output[1])
	time.sleep(.15)
	reset()
	if(gen1[0].fitness<5):
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
turnt.forward(gen1[0].output[0])
turnt.left(90)
turnt.forward(gen1[0].output[1])

window.mainloop()

#------TODO LIST-------
# 1) need to be able to change inputs
# 2) change outputs to angle and foward backwards
# 3) make reproduce work discretely
# 4) add mutation

#other stuff I can't remember

