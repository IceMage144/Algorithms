# coding: utf-8

a = 0x3c6ef372
a
0x6a09e667
def CH(x, y, z):
    return (x & y) ^ ((~x) & z)
for i in range(2):
    for j in range(2):
        for k in range(2):
            print(i, j, k, CH(i, j ,k))
            
def test3(f):
    for i in range(2):
        for j in range(2):
            for k in range(2):
                print(i, j, k, f(i, j ,k))
            
test3(CH)
def MAJ(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)
test3(MAJ)
int b = 0
b = Integer(5)
def ROTRIGHT(x)/
def ROTRIGHT(a, b):
    return (a << b) | (a >> (32-b))
ROTRIGHT(3, 1)
ROTRIGHT(3, 3)
ROTRIGHT(3, 2)
7 << 3
def ROTRIGHT(a, b):
    return (a >> b) | (a << (32-b))
ROTRIGHT(3, 1)
ROTRIGHT(3, 2)
ROTRIGHT(3, 3)
0xf0000000
0xffffffff
ROTRIGHT(1, 1)
2**32
0x80000000
0x80000001
0x800000001
ROTRIGHT(3, 1)
format(ROTRIGHT(3, 1), "x")
format(ROTRIGHT(3, 1), "#x")
0x180000001
3 >> 1
def ROTRIGHT(a, b):
    return ((a >> b) | (a << (32-b))) & 0xffffffff
format(ROTRIGHT(3, 1), "#x")
ROTRIGHT(3, 1)
def EP0(x):
    return ROTRIGHT(x, 2) ^ ROTRIGHT(x, 13) ^ ROTRIGHT(x, 22)
def test1(f):
    for i in range(10):
        print(format(f(i), "#b"))
        
test1(EP0)
def test1(f):
    for i in range(10):
        print(format(f(i), "#x"))
        
        
test1(EP0)
def test1(f):
    for i in range(10):
        print(format(f(i), "#032b"))
        
        
        
test1(EP0)
def test1(f):
    for i in range(10):
        print(format(f(i), "#08x"))
        
        
        
test1(EP0)
def test1(f):
    for i in range(10):
        print(format(f(i), "#034b"))
        
        
        
test1(EP0)
def EP1(x):
    return ROTRIGHT(x, 6) ^ ROTRIGHT(x, 11) ^ ROTRIGHT(x, 25)
test1(EP1)
def SIG0(x):
    return ROTRIGHT(x, 7) ^ ROTRIGHT(x, 18) ^ (x >> 3)
def SIG1(x):
    return ROTRIGHT(x, 17) ^ ROTRIGHT(x, 19) ^ (x >> 10)
test1(SIG0)
test1(SIG1)
(0xa54ff53a + 0x5be0cd19 + EP1(0x510e527f) + CH(0x510e527f, 0x9b05688c, 0x1f83d9ab) + 0x428a2f98) & 0xffffffff
format(2563236514, "#010x")
(0x5be0cd19 + EP0(0x6a09e667) + MAJ(0x6a09e667, 0xbb67ae85, 0x3c6ef372) + EP1(0x510e527f) + CH(0x510e527f, 0x9b05688c, 0x1f83d9ab) + 0x428a2f98) & 0xffffffff
0xffffffff
format(4228417613, "#010x")
test(SIG0)
test(SIGN0)
test1(SIG0)
