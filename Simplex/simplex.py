# A silly implementation of simplex algorithm
#
# It does what you do by hand and still fails in some cases
# This program comes with a problem generator program (problem_gen.py)
# and with an in.txt file with some test cases and their answers

# Input format:
# If you want this system:
# max mx + ny + pz + q
# subj
# ax + by + cz <= d
# ex + fy + gz >= h
#
# You should input (the first number is the number of variables and the second
# is the number of inequalities):
# 3 2
# a b c -d
# -e -f -g h
# m n p q

from fractions import Fraction
from sys import argv

v = False

class Line:
    line = None
    num = -1
    mark = False
    def __init__(self, num_, line_):
        self.line = line_
        self.num = num_
    def __repr__(self):
        s = "["
        for i in range(len(self.line)-1):
            s += f"{self.line[i]}, "
        s += f"{self.line[-1]}] ({self.num})"
        return s
    def pop(self):
        tmp = self.line.pop()
        self.line[-1] = tmp

def decentRepr(v, div=" "):
    s = "["
    for i in range(len(v)-1):
        s += f"{v[i]},{div}"
    s += f"{v[-1]}]"
    return s

def getInput():
    i = input()
    return tuple(i.split())

def findNext(res):
    for i in range(len(res)-1):
        if (res[i] > 0):
            return i
    return -1

def getBetter(mat, var):
    s = 1e10
    i = -1
    for j in range(len(mat)):
        if (mat[j].line[var] != 0 and (not mat[j].mark) and (mat[j].line[-1]/mat[j].line[var] < 0 or (mat[j].line[-1] == 0 and mat[j].line[var] > 0))):
            tmp = -mat[j].line[-1]/mat[j].line[var]
            if (s > tmp):
                s = tmp
                i = j
    return i

def getLine(mat, num):
    m = len(mat)
    for i in range(m):
        if (mat[i].num == num):
            return i
        elif (mat[i].num > num):
            return -1
    return -1


def simplex(n, m, mat, res, v):
    if (v):
        print(decentRepr(mat, "\n"))
        print("Res =", decentRepr(res))
    var = findNext(res)
    step = 0
    while (var >= 0):
        b = getBetter(mat, var)
        if (v):
            print("==================")
            print("Var =", var)
            print("B =", b)
        if (b == -1):
            break
        tmp = mat[b].line[var]
        for i in range(n + m + 1):
            mat[b].line[i] /= tmp
        for i in range(m):
            if (i != b):
                tmp = mat[i].line[var]
                for j in range(m + n + 1):
                    mat[i].line[j] -= mat[b].line[j]*tmp
        tmp = res[var]
        for i in range(m + n + 1):
            res[i] -= mat[b].line[i]*tmp
        res[var] *= 0
        mat[b].num = var
        #mat[b].mark = True
        var = findNext(res)
        last = b
        if (v):
            print(decentRepr(mat, "\n"))
            print("Res =", decentRepr(res))
        step += 1
    if (v): print("Steps =", step)

def maximize(n, m, c, r, v):
    mat = [Line(j+n, [Fraction(1 if (i < n or i == n + m + 1) else 0) for i in range(n + m + 2)]) for j in range(m)]
    fres = [Fraction(0) for i in range(n + m + 2)]
    res = [Fraction(1 if (i < n or i == n + m) else 0) for i in range(n + m + 1)]
    for i in range(m):
        for j in range(n):
            mat[i].line[j] *= c[i][j]
        mat[i].line[n+m+1] *= c[i][n]
        mat[i].line[n+i] = Fraction(1)
        if (c[i][n] > 0):
            mat[i].line[n+m] -= 1
            for j in range(n + m + 2):
                fres[j] -= mat[i].line[j]
    for i in range(n):
        res[i] *= r[i]
    res[n+m] *= r[n]

    if (v):
        print(decentRepr(mat, "\n"))
        print("Res =", decentRepr(res))
        print("\n===== First phase =====")
    simplex(n+1, m, mat, fres, v)
    mat.sort(key = lambda k: k.num)
    for i in range(m):
        mat[i].pop()
    for i in range(n):
        line = getLine(mat, i)
        if (line != -1):
            tmp = res[i]
            for j in range(n+m+1):
                res[j] -= tmp*mat[line].line[j]
            res[i] *= 0
    if (v): print("\n===== Second phase =====")
    simplex(n, m, mat, res, v)

    print("\n================= Answer ====================")
    s = 0
    count = 0
    ret = []
    mat.sort(key = lambda k: k.num)
    for i in range(n):
        if (count < len(mat) and mat[count].num == i):
            tmp = mat[count].line[n+m]
            s -= tmp*r[i]
            ret.append(-tmp)
            count += 1
        else:
            ret.append(0)
    print(decentRepr(ret))
    print(res[-1])
    if (v):
        if (s != res[-1]):
            print(f"Something went wrong {s} != {res[-1]}")
        else:
            print(f"Yay {s} == {res[-1]} !!!")
        aux = []
        for i in range(m):
            s = 0
            for j in range(n):
                s += c[i][j]*ret[j]
            aux.append(s)
        for i in range(m):
            if (aux[i] > -c[i][n]):
                print(f"{aux[i]} > {-c[i][n]} !!!")
            else:
                print(f"{aux[i]} <= {-c[i][n]}")


def main():
    try:
        v = (argv[1] == "-v")
    except IndexError:
        v = False
    (n, m) = getInput()
    n = int(n)
    m = int(m)
    mat = [[None for i in range(n+1)] for j in range(m)]
    res = [None for i in range(n+1)]
    for i in range(m):
        for k, j in zip(getInput(), range(n+1)):
            mat[i][j] = Fraction(k)
    for k, i in zip(getInput(), range(n+1)):
        res[i] = Fraction(k)
    maximize(n, m, mat, res, v)

if __name__ == "__main__":
    main()
