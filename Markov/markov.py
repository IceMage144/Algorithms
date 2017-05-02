from random import *
from sys import *

ignoredChars = [",", ":", ";", "-", "!", "?", "\'", "’", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "`", "/"]
divChars = [".", "\n\n", "\"", "(", ")", "”", "\n", "“"]

class Node:
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.next = {}

    def getNext(self):
        rand = randint(0, self.total)
        valsvec = [val for val in self.next.values()]
        keysvec = [key for key in self.next.keys()]
        if len(keysvec) == 0:
            return None
        pos = 0
        #print(self.next)
        #print(rand)
        while (rand > 0):
            #print(pos)
            rand -= valsvec[pos][0]
            pos += 1
        return keysvec[pos-1]

    def addNext(self, key, ptr):
        if self.next.get(key) == None:
            self.next[key] = [0, ptr]
        self.next[key][0] += 1
        self.total += 1

class Chain:
    def __init__(self):
        self.entries = {}

    def getKey(self, key):
        return self.entries[key]

    def getStart(self):
        rand = randint(0, len(self.entries)-1)
        keysvec = [key for key in self.entries.keys()]
        return keysvec[rand]

    def link(self, key1, key2):
        if self.entries.get(key1) == None:
            self.entries[key1] = Node(key1)
        if self.entries.get(key2) == None:
            self.entries[key2] = Node(key2)
        self.entries[key1].addNext(key2, self.entries[key2])

def takeOutForbs(string):
    ret = string
    for c in ignoredChars:
        ret = ret.replace(c, " ")
    return ret

def divide(string):
    ret = string
    for c in divChars:
        ret = ret.replace(c, "@")
    return ret.split("@")

def main():
    if (len(argv) != 3):
        print("Usage: markov.py <input file> <number of output words>")
        return
    gdict = Chain()
    with open(argv[1], 'r') as f:
        k = f.readlines()
    text = divide("".join(k))
    for i in range(len(text)):
        text[i] = list(filter(None, takeOutForbs(text[i]).split(" ")))
        text[i] = [x.lower() for x in text[i]]
    text = list(filter(None, text))
    #print(text)
    for phrase in text:
        for j in range(len(phrase)-1):
            gdict.link(phrase[j], phrase[j+1])
    #print(gdict.entries)
    ptr = gdict.getStart()
    for i in range(int(argv[2])):
        print(ptr, end=" ")
        ptr = gdict.getKey(ptr).getNext()
        while ptr == None:
            ptr = gdict.getStart()
    print()

main()
