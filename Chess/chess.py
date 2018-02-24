import numpy as np
import copy
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

epoch = 0
side = 40
ratio = 3

# Neural network class for thinking
class Network(object):
    TH = 0.2
    LR = 0.03 # Learning rate
    IR = 0    # Inertia rate
    AR = 1    # Average rate
    def __init__(self, numNeurons):
        self.numNeurons = numNeurons
        self.weights = []
        self.bias = []
        self.last_weights = []
        self.last_bias = []
        self.learn_count = 0
        self.res = []
        self.expected = []
        for i in range(len(numNeurons) - 1):
            self.weights.append(np.random.rand(numNeurons[i], numNeurons[i+1])*2 - 1)
            self.bias.append(np.random.rand(numNeurons[i+1])*2 - 1)
            self.last_weights.append(np.zeros((numNeurons[i], numNeurons[i+1])))
            self.last_bias.append(np.zeros(numNeurons[i+1]))

    def sigmoid(x):
        return 1/(1 + np.exp(-x))

    def dsigmoid(x):
        s = Network.sigmoid(x)
        return s*(1-s)

    def tanh(x):
        return 2/(1 + np.exp(-2*x)) - 1

    def dtanh(x):
        return 1 - Network.tanh(x)**2

    def feedforward(self, inp):
        hVals = np.array(inp)
        for i in range(len(self.weights)):
            hVals = Network.tanh(np.dot(hVals, self.weights[i]) + self.bias[i])
        return hVals

    def learn(self, inp, expected):
        hVals = np.array(inp)
        self.expected.append(np.array(expected))
        self.res.append([copy.deepcopy(hVals)])
        for i in range(len(self.weights)):
            hVals = np.dot(hVals, self.weights[i]) + self.bias[i]
            self.res[self.learn_count].append(copy.deepcopy(hVals))
            hVals = Network.tanh(hVals)

        self.learn_count += 1

        if self.learn_count == Network.AR:
            dw = [np.zeros(self.weights[i].shape) for i in range(len(self.weights))]
            db = [np.zeros(self.bias[i].shape) for i in range(len(self.bias))]
            error = [0 for i in range(Network.AR)]

            # Calculate first error
            for i in range(Network.AR):
                error[i] = (self.expected[i] - Network.tanh(self.res[i][-1]))*Network.dtanh(self.res[i][-1])

            for i in range(len(self.weights) - 1, -1, -1):
                # Calculate average gradient
                for j in range(Network.AR):
                    dw[i] += Network.LR*np.outer(Network.tanh(self.res[j][i]), error[j])
                    db[i] += Network.LR*error[j]
                dw[i] /= Network.AR
                db[i] /= Network.AR

                # Apply inertia
                dw[i] = (1-Network.IR)*dw[i] + Network.IR*self.last_weights[i]
                db[i] = (1-Network.IR)*db[i] + Network.IR*self.last_bias[i]

                # Calculate next error
                for j in range(Network.AR):
                    error[j] = (self.weights[i]@error[j])*Network.dtanh(self.res[j][i])

            for i in range(len(self.weights)):
                # Sum gradients
                self.weights[i] += dw[i]
                self.last_weights[i] = copy.deepcopy(dw[i])
                self.bias[i] += db[i]
                self.last_bias[i] = copy.deepcopy(db[i])

            self.res = []
            self.expected = []
            self.learn_count = 0

    def copy(self):
        return copy.deepcopy(self)

def zero(x):
    if (type(x) == list or type(x) == np.ndarray) and len(x) != 0:
        if type(x[0]) == list or type(x[0]) == np.ndarray:
            for i in range(len(x)):
                zero(x[i])
        elif type(x[0]) == int:
            for i in range(len(x)):
                x[i] = 0

def xor(x):
    return ((x[0] > 0 and x[1] < 0) or (x[0] < 0 and x[1] > 0))

def dist(x):
    return x[0]**2 + x[1]**2

def square(x):
    s = math.sqrt(2)/2
    return x[0] < s and x[0] > -s and x[1] < s and x[1] > -s

def main():
    nn = Network([2, 2, 1])
    x = [[[0, 0], [-1]],
         [[0, 1], [1]],
         [[1, 0], [1]],
         [[1, 1], [-1]]]
    x2 = [[[0, 0, 0, 0, 0], [-1]],
         [[0, 1, 0, 1, 0], [1]],
         [[1, 0, 1, 0, 0], [1]],
         [[1, 1, 1, 1, 1], [-1]]]
    fig, ax = plt.subplots(figsize=(5, 5))
    mat = [[[ratio*(2*x/side - 1), ratio*(1 - 2*y/side)] for x in range(side)] for y in range(side)]
    # mat2 = [[[ratio*(2*x/side - 1), ratio*(1 - 2*y/side), (ratio*(2*x/side - 1))**2, (ratio*(1 - 2*y/side))**2, ratio*(1 - 2*y/side)*ratio*(2*x/side - 1)] for x in range(side)] for y in range(side)]
    c = ax.imshow([[nn.feedforward(mat[i][j])[0] for i in range(side)] for j in range(side)],
                  interpolation='nearest',
                  aspect='auto',
                  cmap='RdYlGn')
    epoch_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    def update():
        global epoch
        for i in range(10):
            #-------------------------------------------
            s = random.sample(x, 1)[0]
            nn.learn(s[0], s[1])
            #-------------------------------------------
            # theta = random.random()*6.2831
            # r = random.random()
            # p = [r*math.cos(theta), r*math.sin(theta)]
            # p.append(p[0]**2)
            # p.append(p[1]**2)
            # p.append(p[0]*p[1])
            # nn.learn(p, [1 if r < 0.5 else -1])
            #-------------------------------------------
            # p = [ratio*(random.random()*2-1), ratio*(random.random()*2-1)]
            # p.append(p[0]**2)
            # p.append(p[1]**2)
            # p.append(p[0]*p[1])
            # nn.learn(p, [1 if xor(p) else -1])
            #-------------------------------------------
            # theta = 5*math.pi*(random.random()*2 - 1)
            # p = [0.05*theta*math.cos(math.fabs(theta)), 0.05*theta*math.sin(math.fabs(theta))]
            # p.append(p[0]**2)
            # p.append(p[1]**2)
            # p.append(p[0]*p[1])
            # nn.learn(p, [1 if theta >= 0 else -1])
            #-------------------------------------------
        epoch += 100
        yield [[nn.feedforward(mat[i][j])[0] for i in range(side)] for j in range(side)]
    def plot(update):
        global epoch
        c.set_data(update)
        epoch_text.set_text(f"Epoch = {epoch}")
        return c, epoch_text
    ani = FuncAnimation(fig, plot, update, interval=50)
    # t = np.arange(0.0, 5*math.pi, 0.01)
    # sx = side*0.05*t*np.cos(t)/ratio
    # sy = side*0.05*t*np.sin(t)/ratio
    # ax.plot(side/2 - sx, side/2 - sy, color="blue")
    # ax.plot(side/2 + sx, side/2 + sy, color="red")
    plt.ylim(0, side)
    plt.xlim(0, side)
    #plt.axis('off')
    plt.show()
    print(nn.weights)
    print(nn.bias)
    p = input("Point: ")
    while p != "":
        p = [float(i) for i in p.split()]
        print(p)
        print(nn.feedforward(p))
        p = input("Point: ")

def test():
    nn = Network([2, 3, 2, 1])
    x = [[[0, 0], [-1]],
         [[0, 1], [1]],
         [[1, 0], [1]],
         [[1, 1], [-1]]]
    for i in range(100):
        #p = [random.random()*2 - 1, random.random()*2 - 1]
        theta = random.random()*6.2831
        r = random.random()
        p = [r*math.cos(theta), r*math.sin(theta)]
        print("Before:", r, nn.feedforward(p))
        nn.learn(p, [1 if r < 0.5 else -1])
        print("After:", r, nn.feedforward(p))
        #s = random.sample(x, 1)[0]
        #s = [[1, 1], [0.5]]
        #print("Before:", s[0], nn.feedforward(s[0]))
        #nn.learn(s[0], s[1])
        #print("After:", s[0], nn.feedforward(s[0]))
        #print("==================================")
    print(nn.weights)
    print(nn.bias)
    for s in x:
        print(s[0], nn.feedforward(s[0]))
    p = input("Point: ")
    while p != "":
        p = [float(i) for i in p.split()]
        print(p)
        print(nn.feedforward(p))
        p = input("Point: ")


if __name__ == '__main__':
    main()
