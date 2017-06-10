from PIL import Image
import numpy as np
import json
from sys import argv

IMGSIZE = 64*64

class Neuron:
    # For input at the constructor method:
    # "method" can be either "matrix" or "dict"
    # If "matrix", the arguments are:
    #   - arg1: the numpy matrix corresponding to the image
    #   - arg2: the return value desired
    # If "dict", the argument is:
    #   - arg1: a dictionary containing the matrix corresponding to the image,
    #           with key "Matrix", and the desired return value, with the key
    #           "Return"
    def __init__(self, arg1, arg2=None, method="matrix"):
        if method == "matrix":
            self.mat = arg1.copy()
            self.ret = arg2
        elif method == "dict":
            self.mat = np.asarray(arg1["Matrix"].copy())
            self.ret = arg1["Return"]
        else:
            print("Oh-oh")

    def compare(self, inp):
        sub = self.mat - inp
        count = np.count_nonzero(sub)
        return [self.ret, IMGSIZE-count, count]

    def toDict(self):
        dic = {}
        dic["Return"] = self.ret
        dic["Matrix"] = self.mat.tolist()
        return dic

def Color(string, num):
    return (f"\033[1;{num}m{string}\033[0m")

def loadDatabase(fileName):
    try:
        print(Color("Loading database...", 33))
        jsonList = json.load(open(fileName))[1:]
        ret = []
        for dic in jsonList:
            ret.append(Neuron(dic, method="dict"))
        print(Color("Finish loading", 32))
        return ret
    except FileNotFoundError:
        print(Color("Database not found", 31))
        return []

def saveDatabase(fileName, neuList):
    jsonList = []
    jsonList.append(len(neuList))
    for neu in neuList:
        jsonList.append(neu.toDict())
    with open(fileName, "w+") as f:
        f.write(json.dumps(jsonList, separators=(", ", ":")))
    print(Color("Saved database", 32))

def askNeurons(img, neuList):
    if not neuList:
        return -1
    resArr = []
    for neuron in neuList:
        resArr.append(neuron.compare(img))
    resArr.sort(key=lambda x : -x[1])
    print(resArr)
    return resArr[0][0]

def main():
    try:
        countRight = 0
        countWrong = 0
        neuList = loadDatabase(argv[1])
        for imgFile in argv[2:]:
            img = Image.open(imgFile).resize((64, 64)).convert("L")
            imgData = (np.asarray(img) > 128) * 1
            res = askNeurons(imgData, neuList)
            ans = int(imgFile[len(imgFile)-5])
            if res != ans:
                neuList.append(Neuron(imgData, ans))
                countWrong += 1
                print(Color("Wrong answer:", 31))
                print("Right:", ans)
                print("Returned:", res)
            else:
                countRight += 1
                print(Color("Right answer:", 32))
                print("Right:", ans)
                print("Returned:", res)
        saveDatabase(argv[1], neuList)
        print("Rights:", countRight)
        print("Wrongs:", countWrong)
    except IndexError:
        print("Usage: digitsRecoProb <input database save/load> <image 1> <image 2> ...")
        raise
        return 0

if __name__ == "__main__":
    main()
