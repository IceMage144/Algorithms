import math

def norm(mat):
    s = 0
    for i in mat:
        for j in i:
            s += j**2
    return math.sqrt(s)

def multMat(mat1, mat2):
    ret = [[0 for i in range(len(mat2[0]))] for j in range(len(mat1))]
    for i in range(len(mat1)):
        for k in range(len(mat2[0])):
            s = 0
            for j,l in zip(range(len(mat1[0])), range(len(mat2))):
                s += mat1[i][j]*mat2[l][k]
            ret[i][k] = s
    return ret

def invDiag(mat):
    ret = [[0 for i in range(len(mat))] for j in range(len(mat))]
    [[0]*len(mat)]*len(mat)
    for i in range(len(mat)):
        ret[i][i] = (0 if mat[i][i] == 0 else 1/mat[i][i])
    return ret

def diagRemainder(mat):
    ret = [[0 for i in range(len(mat))] for j in range(len(mat))]
    for i in range(len(mat)):
        for j in range(len(mat)):
            ret[i][j] = (0 if i == j else mat[i][j])
    return ret

def subMat(mat1, mat2):
    ret = [[0 for i in range(len(mat1[0]))] for j in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            ret[i][j] = mat1[i][j] - mat2[i][j]
    return ret

def main():
    '''A = [[10, -1, 2, 0],
         [-1, 11, -1, 3],
         [2, -1, 10, -1],
         [0, 3, -1, 8]]
    b = [[6], [25], [-11], [15]]
    x = [[0], [0], [0], [0]]'''
    n = int(input("Input the number of variables:\n"))
    err = float(input("Input the precision of the algorithm:\n"))
    m = int(input("Input the max number of iterations:\n"))
    A = [[0 for i in range(n)] for j in range(n)]
    print("=== Starting matrix A ===")
    for i in range(n):
        for j in range(n):
            A[i][j] = float(input(f"Enter a{i+1}{j+1}: "))
    print("=== Finished matrix A ===")
    b = [[0] for i in range(n)]
    print("=== Starting b vector ===")
    for i in range(n):
        b[i][0] = float(input(f"Enter b{i+1}: "))
    print("=== Finished b vector ===")
    x = [[0] for i in range(n)]
    print("=== Starting guess vector ===")
    for i in range(n):
        x[i][0] = float(input(f"Enter x{i+1}: "))
    print("=== Finished guess vector ===")
    counter = 0
    xMem = [[0] for i in range(n)]
    print(f"x{counter}:", x)
    xMem = x.copy()
    DInv = invDiag(A)
    #print("DInv:", DInv)
    R = diagRemainder(A)
    #print("R:", R)
    T = multMat(DInv, R)
    #print("T:", T)
    C = multMat(DInv, b)
    #print("C:", C)
    M = multMat(T, xMem)
    #print("M:", M)
    x = subMat(C, M)
    s = abs(norm(x)-norm(xMem))
    counter += 1
    while (counter < m and s > err):
        print("=============================================")
        print(f"x{counter}:", x)
        xMem = x.copy()
        DInv = invDiag(A)
        #print("DInv:", DInv)
        R = diagRemainder(A)
        #print("R: ", R)
        T = multMat(DInv, R)
        #print("T: ", T)
        C = multMat(DInv, b)
        #print("C: ", C)
        x = subMat(C, multMat(T, xMem))
        s = abs(norm(x)-norm(xMem))
        counter += 1
    print("Result: ", x)
    for i in range(len(x)):
        x[i][0] = round(x[i][0], 4)
    print("Rounded answer: ", x)

if __name__=="__main__":
    main()
