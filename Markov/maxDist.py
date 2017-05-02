from itertools import *

vect = [12.02, 9.1, 8.12, 7.68, 7.31, 6.28, 6.02, 5.92, 4.32, 3.98, 2.88, 2.71, 2.61, 2.3, 2.11, 2.09, 2.03, 1.82, 1.49, 1.11, 0.69, 0.17, 0.11, 0.1, 0.07]
lett = [4, 19, 0, 14, 8, 13, 18, 17, 7, 3, 11, 20, 2, 12, 5, 24, 22, 6, 15, 1, 21, 10, 23, 16, 9, 25]
strs = 'abcdefghijklmnopqrstuvwxyz'
ordv = [8.12, 1.11, 2.61, 3.98, 12.02, 2.11, 1.82, 4.32, 7.31, 0.07, 0.17, 2.88, 2.3, 6.28, 7.68, 1.49, 0.1, 5.92, 6.02, 9.1, 2.71, 0.69, 2.03, 0.11, 2.09]
ordl = [i for i in range(26)]
corr = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

def main():
    nums = 6
    base = [x for x in range(1, nums)]
    vres = []
    maxdist = 0
    for v1 in permutations(base):
        for v2 in permutations(base):
            dist = 0
            for o,e in zip(v1, v2):
                dist += (o-e)**2/e
            if dist > maxdist:
                vres = [[v1, v2]]
                maxdist = dist
            if dist == maxdist:
                vres.append([v1, v2])
    print(vres)
    print(maxdist)

def calcMaxDist():
    rvect = list(reversed(vect))
    dist = 0
    for o,e in zip(rvect, vect):
        dist += (o-e)**2/e
    print(dist)

"""
def troca (vect, pos1, pos2):
    aux = vect[pos1]
    vect[pos1] = vect[pos2]
    vect[pos2] = aux

def bubbleSort(vect1, vect2):
    count = 0
    tam = len(vect1)
    while (count != tam-1):
        count = 0
        for i in range(tam-1):
            if (vect1[i] > vect1[i+1]):
                troca(vect1, i, i+1)
                troca(vect2, i, i+1)
            else:
                count += 1
"""

def calcDist(vec1, vec2):
    dist = 0
    for o,e in zip(vec1, vec2):
        dist += (o-e)**2/e
    return dist

def shift(v):
    ret = v[1:len(v)]
    ret.append(v[0])
    return ret

def analize():
    tester = ordv.copy()
    for i in range(26):
        tester = shift(tester)
        print(i, " : ", calcDist(tester, ordv))

def realCase():
    f = "out.txt"
    res = [0]*26
    with open(f, 'r') as g:
        k = g.readlines()
    k = "".join(k).strip().replace(" ", "")
    for l in k:
        res[corr[l]] += 1
    for i in range(26):
        res[i] = 100*res[i]/len(k)
    print(res)
    print("The distance is: ", calcDist(res, ordv))

#main()
realCase()
#calcMaxDist()
#analize()
