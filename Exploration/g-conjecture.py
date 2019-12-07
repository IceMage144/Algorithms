import numpy as np

def generatePascalMatrix(n):
    m = np.eye(n)
    for i in range(n-1, -1, -1):
        for j in range(n-2, i, -1):
            m[j][i] = m[j][i+1] + m[j+1][i+1]
        m[n-1][i] = 1
    for i in range(n):
        for j in range(i):
            m[i][j] *= 1 if (i + j)%2 == 0 else -1
    return m

def main():
    np.set_printoptions(suppress=True)
    f = np.array([1, 6, 15, 20, 15])
    P = generatePascalMatrix(6)
    print(P)
    #print(P@f)
    s = np.array([1, 4, 5, 4, 1])
    Pinv = np.linalg.inv(P)
    #print(Pinv@s)

if __name__ == '__main__':
    main()
