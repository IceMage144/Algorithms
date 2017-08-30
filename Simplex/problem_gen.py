# Generates a system of inequalities for simplex.py
#
# This gets an line argument, that is the number of variables at your system,
# and prints the system formated as an input for simplex.py

import sys

def main():
    try:
        n = int(sys.argv[1])
    except IndexError:
        print("problem_gen: You should give me the number of variables you want")
    print(n, n)
    r = 1 - 2*n
    for i in range(n):
        for j in range(n):
            if (i == j):
                print(1, end=" ")
            else:
                print(2, end=" ")
        print(r)
    for i in range(n):
        print(1, end=" ")
    print(0)

if __name__ == "__main__":
    main()
