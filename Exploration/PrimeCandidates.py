# 1 : 1/2                = 0.5                 = 1/2
# 2 : 2/6                = 0.3333333333333333  = 1/2 * 2/3
# 3 : 8/30               = 0.26666666666666666 = 1/2 * 2/3 * 4/5
# 4 : 48/210             = 0.22857142857142856 = 1/2 * 2/3 * 4/5 * 6/7
# 5 : 480/2310           = 0.2077922077922078  = 1/2 * 2/3 * 4/5 * 6/7 * 10/11
# 6 : 5760/30030         = 0.1918081918081918  = 1/2 * 2/3 * 4/5 * 6/7 * 10/11 * 12/13
# 7 : 92160/510510       = 0.18052535699594524 = 1/2 * 2/3 * 4/5 * 6/7 * 10/11 * 12/13 * 16/17
# 8 : 1658880/9699690    = 0.17102402241721126 = 1/2 * 2/3 * 4/5 * 6/7 * 10/11 * 12/13 * 16/17 * 18/19
# 9 : 36495360/223092870 = 0.16358819535559338 = 1/2 * 2/3 * 4/5 * 6/7 * 10/11 * 12/13 * 16/17 * 18/19 * 22/23

def listPrimes(num):
    l = []
    p = 2
    while len(l) != num:
        pss = False
        for i in l:
            if p%i == 0:
                pss = True
                break
        if not pss:
            l.append(p)
        p += 1
    return l

def findCandidates(primes, mx):
    cands = []
    for i in range(mx):
        pss = False
        for num in primes:
            if i%num == 0:
                pss = True
                break
        if not pss:
            cands.append(i)
    return cands

def prod(l):
    res = 1
    for num in l:
        res *= num
    return res

def main():
    for i in range(10):
        primes = listPrimes(i)
        mx = prod(primes)
        cands = findCandidates(primes, mx)
        print(f"{i} : {len(cands)}/{mx} = {len(cands)/mx}")
    # print(primes)
    # print(cands)

if __name__ == '__main__':
    main()
