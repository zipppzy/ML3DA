import math

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
                if (activation>=stepLimit):
                    return 1
                else: return 0
