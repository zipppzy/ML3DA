import math
import abc
import random
import operator
from decimal import Decimal,getcontext
import bpy

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
                getcontext().prec=100
                if(len(inputs)==self.numInputs and len(self.weights)>0):
                        activation=0
                        for i in range(self.numInputs):
                                activation+=inputs[i]*self.weights[i]
                        if(self.activationFunc=="sum"):
                                return activation
                        if(self.activationFunc=="sigmoid"):
                                
                                if(activation<-709.7):
                                        activation=-709.7
                                #print("activation: "+str(activation))
                                return 1/(1+(math.e**((activation*-1)/(self.sigmoidConstant))))
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


class GenAlg(abc.ABC):
        
        
        def __init__(self,numGens,numIndivs,mutationRate,culledPercent,structure,numInputs,activationFunc,crossoverRate=1,sigmoidConstant=1,stepLimit=0):
                global show
                # GenAlg(1,2,.1,.1,.1,[2,3],1,"sigmoid")
                self.numGens=numGens
                self.numIndivs=numIndivs
                self.crossoverRate=crossoverRate
                self.mutationRate=mutationRate
                self.culledPercent=culledPercent
                self.structure=structure
                self.numInputs=numInputs
                self.activationFunc=activationFunc
                self.sigmoidConstant=sigmoidConstant
                self.stepLimit=stepLimit
                self.gen=[]
                for i in range(numIndivs):
                        self.gen.append(NeuralNet(structure,numInputs,activationFunc,sigmoidConstant,stepLimit))
                for i in self.gen:
                        i.setWeights(self.randomWeights())
                        i.fitness=self.fitnessFunction(i)
                for i in range(numGens):
                        self.cull()
                        self.reproduce()
                        print(self.gen[0].fitness)
                        if(i%10==0):
                            show=True
                            self.fitnessFunction(self.gen[0])
                            show=False
                        

                

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
        def fitnessFunction(self,a):
                """returns a number indicating the fitness of a given neuralNet"""
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
                        children=self.crossover(self.gen[choice1].getWeights(),self.gen[choice2].getWeights())
                        self.gen.append(NeuralNet(self.structure,self.numInputs,self.activationFunc,self.sigmoidConstant,self.stepLimit))
                        self.gen[len(self.gen)-1].setWeights(children[0])
                        self.gen[len(self.gen)-1].fitness=self.fitnessFunction(self.gen[len(self.gen)-1])
                        self.gen.append(NeuralNet(self.structure,self.numInputs,self.activationFunc,self.sigmoidConstant,self.stepLimit))
                        self.gen[len(self.gen)-1].setWeights(children[1])
                        self.gen[len(self.gen)-1].fitness=self.fitnessFunction(self.gen[len(self.gen)-1])
                if(len(self.gen)>self.numIndivs):
                        del self.gen[len(self.gen)-1]
                
        def crossover(self,A,B):
                weightsA=self.threeDtoOneD(A)
                weightsB=self.threeDtoOneD(B)
                cutPoint=int(random.random()*(len(weightsA)-1))+1
                piece1A=weightsA[0:cutPoint]
                piece2A=weightsA[cutPoint:len(weightsA)]
                piece1B=weightsB[0:cutPoint]
                piece2B=weightsB[cutPoint:len(weightsB)]
                child1=piece1A+piece2B
                child2=piece1B+piece2A
                for i in child1:
                        if(random.random()<self.mutationRate):
                                i=random.random()
                child2=piece1B+piece2A
                for i in child2:
                        if(random.random()<self.mutationRate):
                                i=random.random()
                child1=self.oneDtoThreeD(child1)
                child2=self.oneDtoThreeD(child2)
                return [child1,child2]



        

        def threeDtoOneD(self,three):
                one=[]
                for i in three:
                        for j in i:
                                for k in j:
                                        one.append(k)
                return one
        def oneDtoThreeD(self,one):
                oneCounter=0
                three=[]
                for i in range(len(self.structure)):
                        three.append([])
                for i in range(len(self.structure)):
                        
                        for j in range(self.structure[i]):
                                
                                neuronWeights=[]
                                if (i==0):
                                        for k in range(self.numInputs):
                                                neuronWeights.append(one[oneCounter])
                                                oneCounter+=1
                                                
                                elif(i>0):
                                        for k in range (self.structure[i-1]):
                                                neuronWeights.append(one[oneCounter])
                                                oneCounter+=1
                                three[i].append(neuronWeights)
                return three
class myGenAlg(GenAlg):
        #input is cartesian[x,y,z] output is cylindrical[r,theta,z] http://electron9.phys.utk.edu/vectors/3dcoordinates.htm

        def fitnessFunction(self,a):
                global show
                #moves
                pointA=Point(random.random()*10,random.random()*10,random.random()*10)
                #destination
                pointB=Point(random.random()*10,random.random()*10,random.random()*10)
                
                while(pointA.distance(pointB)<20):
                        pointB=Point(random.random()*100,random.random()*100,random.random()*100)
                count=0
                while(pointA.distance(pointB)>10 and count<1000):
                        global show
                        startPoint=pointA
                        #mebe want to change scaling
                        output=a.getOutput([((pointB.x-pointA.x)*100)-50,(pointB.y-pointA.y)*(2*math.pi),((pointB.z-pointA.z)*100)-50])
                        pointA.x+=output[0]*math.cos(output[1])
                        pointA.y+=output[0]*math.sin(output[1])
                        pointA.z+=output[2]
                        count+=1
                        if(show and count<30):
                            visualize(startPoint,pointB,pointA)
                            print("animating")
                        #print(pointA.distance(pointB))
                #print("count: "+count)
                return -count



class Point():
        def __init__(self,x,y,z):
                self.x=x
                self.y=y
                self.z=z
        def distance(self,B):
                return math.sqrt(((B.x-self.x)**2)+((B.y-self.y)**2)+((B.z-self.z)**2))
def visualize(startPos,goalPos,movePos):
    global currentFrame
    start=bpy.data.objects["Start"]
    goal=bpy.data.objects["Goal"]
    start.location=(startPos.x,startPos.y,startPos.z)
    goal.location=(goalPos.x,goalPos.y,goalPos.z)
    start.keyframe_insert(data_path="location",frame=currentFrame)
    start.location=(movePos.x,movePos.y,movePos.z)
    currentFrame+=10
    start.keyframe_insert(data_path="location",frame=currentFrame)
def reset():
    bpy.data.objects["Start"].animation_data_clear()

print("start")
currentFrame=1
show=False
reset()
#numGens,numIndivs,crossoverRate,mutationRate,culledPercent,structure,numInputs,activationFunc,sigmoidConstant=1,stepLimit=0
g=myGenAlg(20,50,.05,.1,[3,5,3],3,"sigmoid")
print("end")
#visualize(Point(0,0,0),Point(5,5,5),Point(-5,0,5))



                




