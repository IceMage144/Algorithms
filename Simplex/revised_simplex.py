# A silly implementation of simplex algorithm
#
# It does what you do by hand and still fails in some cases
# This program comes with a problem generator program (problem_gen.py)
# and with an in.txt file with some test cases and their answers

# Input format:
# If you want this system:
# max mx + ny + pz
# subj
# ax + by + cz <= d
# ex + fy + gz >= h
#
# You should input (the first number is the number of variables and the second
# is the number of inequalities):
# 3 2
# a b c d
# -e -f -g -h
# m n p

from fractions import Fraction
from sys import argv
import numpy as np

v = False

def decentRepr(v, div=" "):
    s = "["
    for i in range(len(v)-1):
        s += f"{v[i]},{div}"
    s += f"{v[-1]}]"
    return s

def getInput():
    i = input()
    return tuple(map(float, i.split()))

def findNext(cr):
    for i in range(len(cr)):
        if (cr[i] > 0):
            return i
    return -1

def getMinIdx(coefs, consts):
    mn = 1e30
    minIdx = -1
    for i in range(len(coefs)):
        if ((coefs[i] > 0 and consts[i] >= 0) or (coefs[i] < 0 and consts[i] < 0)):
            if (consts[i]/coefs[i] < mn):
                mn = consts[i]/coefs[i]
                minIdx = i
    return minIdx

def translate(xb, consts, n):
    res = np.zeros(n+len(xb))
    for i in range(len(xb)):
        res[xb[i]] = consts[i]
    return tuple(np.split(res, [n]))

def rsimplex(n, m, N, b, cn, v):
    c = cn.copy()
    N1 = N.copy()
    B = np.identity(m)
    Binv = np.linalg.inv(B)
    cb = np.zeros(m)
    cr = cn.copy()
    xn = np.arange(n)
    xb = np.arange(n, m+n)
    if (v):
        print("cr:\n", cr)
    while ((cr > 0).any()):
        if (v):
            print("N:\n", N)
            print("B:\n", B)
            print("cb:\n", cb)
            print("cn:\n", cn)
            print("xb:\n", xb)
            print("xn:\n", xn)
        idx = findNext(cr)
        consts = Binv@b
        coefs = Binv@(N.T[idx])
        if (v):
            print("coefs:\n", coefs)
            print("consts:\n", consts)
        minIdx = getMinIdx(coefs, consts)
        if (minIdx == -1):
            print("Watashi wa mou shindeiru!!")
            return False
        if (v):
            print("base idx: ", idx)
            print("min idx: ", minIdx)
        mem = N.T[idx].copy()
        N.T[idx] = B.T[minIdx]
        B.T[minIdx] = mem
        mem = xn[idx]
        xn[idx] = xb[minIdx]
        xb[minIdx] = mem
        mem = cn[idx]
        cn[idx] = cb[minIdx]
        cb[minIdx] = mem
        Binv = np.linalg.inv(B)
        cr = cn - cb@Binv@N
        if (v):
            print("cr:\n", cr)
    consts = Binv@b
    xRes, auxRes = translate(xb, consts, n)
    print("============================================================")
    print("Checking...")
    o = np.array([N1@xRes, b])
    print(o.T)
    print(o[0] <= o[1])
    return (xRes, auxRes, c@xRes)

def main():
    try:
        v = (argv[1] == "-v")
    except IndexError:
        v = False
    (n, m) = getInput()
    n = int(n)
    m = int(m)
    A = np.zeros((m, n))
    b = np.zeros(m)
    c = np.zeros(n)
    for i in range(m):
        inp = list(getInput())
        for k, j in zip(inp, range(n)):
            A[i][j] = k
        b[i] = inp[n]
    for k, i in zip(getInput(), range(n)):
        c[i] = k
    xRes, auxRes, z = rsimplex(n, m, A, b, c, v)
    if (v):
        print("============================================================")
    print("Main variables result:\n", xRes)
    print("Auxiliar variables result:\n", auxRes)
    print("Maximum value: ", z)

if __name__ == "__main__":
    main()
