import math
import matplotlib.pyplot as plt
import numpy as np

'''
This program was made to analyze the "Collatz conjecture" or the "3n+1
conjecture" (https://en.wikipedia.org/wiki/Collatz_conjecture).
To make this program, I analized the result of all the aplications of the
function at an initial number, eg:
	   ┌ 3x+1  , if x is odd
f(x) = ┤
	   └ x/2   , if x is even

If we have f(f(f(f(f(f(f(3))))))) = 1 we can expand this to get
(3*3^2 + 5)/2^5 = 1
3*3^2 + 5 = 2^5

In fact, we can see a pathern here. Expanding the successive aplications of the
function we get:

x*3^w + z = 2^a
Where:
	- x is the initial number
	- w is the number of odd numbers found during the steps or the number of
aplications of the odd rule of the function (f(x) = 3x+1). Also called "three"
or "power of the three" in this program.
	- z is a number of the form sum[i from 0 to w-1] 2^(b_i)*3^i, where all b_i
are zero or positive integers and b_(i-1) > b_i > b_(i+1). Also called
"3-smooth" in this program (sequence A213539 at OEIS).
	- a is the number of even numbers found or the number of aplications of the
even rule of the function (f(x) = x/2). Also called "two" or "power of the two"
in this program.


Esse programa foi feito para analizar a "Conjectura de Collatz" ou a "Conjectura
3n+1" (https://en.wikipedia.org/wiki/Collatz_conjecture).
Para fazer esse programa, eu analizei o resultado de todas as aplicações da
função em um número inicial, ex:
	   ┌ 3x+1  , se x for ímpar
f(x) = ┤
	   └ x/2   , se x for par

Se tivermos f(f(f(f(f(f(f(3))))))) = 1 nós podemos expandir isso para obter
(3*3^2 + 5)/2^5 = 1
3*3^2 + 5 = 2^5

De fato, podemos ver um padrão aqui. Expandindo as sucessivas aplicações da
função nós temos:

x*3^w + z = 2^a
Onde:
	- x é o número inicial
	- w é o número de ímpares achados durante os passos ou o número de
aplicações da regra para ímpares da função (f(x) = 3x+1). Também é chamado de
"three" ou "power of the three" nesse programa.
	- z é um número da forma sum[i from 0 to w-1] 2^(b_i)*3^i, onde todos os
b_i são zero ou inteiros positivos e b_(i-1) > b_i > b_(i+1). Também chamado de
"3-smooth" nesse programa (sequência A213539 na OEIS).
	- a é o número de pares achados durante os passos ou o número de aplicações
da regra para pares da função (f(x) = x/2). Também chamado de "two" ou "power
of the two" nesse programa.
'''

gr = 1.6180339
fgr = 1.5873
lgt = math.log(2, 3)

def sorting (mat):
	count = 1
	while (count > 0):
		count = 0
		for i in range(len(mat)-1):
			if (mat[i][0] > mat[i+1][0]):
				mat[i], mat[i+1] = mat[i+1], mat[i]
				count += 1
	return mat

def specprint (mat):
	for i in range(len(mat)):
		print(mat[i][0], mat[i][1])

def nexttwo (top, vec, dig):
	num = 0
	aux = 0
	if dig == 0:
		vec[0] += 1
	if dig >= len(vec):
		return 0, []
	while (aux < len(vec) and vec[aux] != -1):
		aux += 1
	for i in range(aux):
		num += (3**i)*(2**vec[i])
	if (num > top):
		vec[dig] += 1
		for i in range(dig, 0, -1):
			vec[i-1] = vec[i] + 1
		num, vec = nexttwo(top, vec, dig+1)
	return num, vec

'''
This function finds "3-smooth"s.

Essa função acha "3-smooth"s.
'''
def tsmooth ():
	top = int(input("Choose the maximum number:\n"))
	final = []
	nonrept = []
	two = []
	res = 0
	toppow = 0
	count = 0
	aux = 0
	while (3**toppow < top):
		toppow += 1
	while (len(two) < toppow):
		two.append(-1)
	two[0] += 1
	res = 1
	while (res != 0):
		final.append([res, [two[i] for i in range(toppow)]])
		res, two = nexttwo(top, two, 0)
	specprint(final)
	print("==============================")
	final = sorting(final)
	specprint(final)
	print("Included numbers:")
	for i in range(len(final)):
		if ((i+1 < len(final) and final[i][0] != final[i+1][0]) or (i+1 >= len(final))):
			print(final[i][0], "/\n"[i == len(final)-1], end="")
			nonrept.append(final[i][0])
	print("Not included:")
	while (count < top):
		if (aux < len(nonrept)):
			if (nonrept[aux] != count):
				print(count, end="")
				if (count%3 != 0):
					print("* /", end="")
				else:
					print(" /", end="")
			else:
				aux += 1
		else:
			print(count, end="")
			if (count%3 != 0):
				print("* /", end="")
			else:
				print(" /", end="")
		count += 1
	print("\nListed twice")
	for i in range(len(final)-1):
		if (final[i][0] == final[i+1][0]):
			print(final[i][0], "/", end="")
	print()

'''
This function calculates the number of steps of an initial number and gives
detailed information about the route it went though, like the numbers "a",
"w" and "z", the sum of the steps (a+w), the difference of the steps (a-w) and
the order they appear.

Essa função calcula o número de passos de um número inicial e dá informaçoẽs
detalhadas sobre seu percurso, como os números "a", "w" e "z", a soma do número
de passos (a+w), a diferença do número de passos (a-w) e a ordem em que eles
aparecem.
'''
def collatz (arg):
	if arg == -1:
		num = int(input("Choose a number:\n"))
	else:
		num = arg
	mem = num
	two = 0
	three = 0
	while num != 1:
		if num%2 == 0:
			if arg == -1:
				print("even", num)
			num = int(num/2)
			two += 1
		else:
			if arg == -1:
				print("odd ", num)
			num = 3*num + 1
			three += 1
	if arg == -1:
		print("============== Final results ==============")
		print("- Inicial number:                  ", mem)
		print("- Number of divisions (x/2):       ", two)
		print("- Number of multiplications (3x+1):", three)
		print("- Sum of steps:                    ", two+three)
		print("- Difference of the steps:         ", two-three)
		print("- 3-smooth associated:             ", 2**two-mem*3**three)
		return 0, 0
	else:
		return two, three

def countdigs (num):
	return(len(str(num)))

'''
This function makes exactly what the "collatz" function do with various numbers,
but it doesn't gives information about the route.

Essa função faz exatamente o que a função "collatz" faz com vários números,
porém ela não dá informações sobre a percurso.
'''
def mcollatz ():
	two = 0
	three = 0
	aux = 0
	digits = [0, 0, 0, 0, 0]
	top = int(input("Choose the maximum number:\n"))
	print("number    twos    threes    total    difference    3-smooth")
	for i in range(3, top, 2):
		two, three = collatz(i)
		digits[0] = countdigs(i)
		digits[1] = countdigs(two)
		digits[2] = countdigs(three)
		digits[3] = countdigs(two+three)
		digits[4] = countdigs(two-three)
		print(i, end="")
		for j in range(10-digits[0]):
			print(" ", end="")
		print(two, end="")
		for j in range(8-digits[1]):
			print(" ", end="")
		print(three, end="")
		for j in range(10-digits[2]):
			print(" ", end="")
		print(two+three, end="")
		for j in range(9-digits[3]):
			print(" ", end="")
		print(two-three, end="")
		for j in range(14-digits[4]):
			print(" ", end="")
		aux = 2**two - i*(3**three)
		# print(two, three, 2**two, 3**three, i)
		print(aux)

'''
This function takes as input the "w" and the "z" and find the initial numbers
"x" and their "a" value that solves the equation.
Some notes:
- I put a limit of a < 50 on this function due to the overflow, but the values
of "a" that solve the equation follow a pattern, just take the first "a" value
that solves it and add k*2*3^(w-1), for any positive integer "k".


Essa função recebe os valores "w" e "z" e acha os números iniciais "x" e seu
valor de "a" que resolvem a equação.
Algumas notas:
- Eu coloquei um limite de a < 50 nessa função por causa do overflow, porém
os valores de "a" que resolvem a equação seguem um padrão, é só pegar o
primeiro valor de "a" que resolve a equação e adicionar k*2*3^(w-1), para
qualquer "k" inteiro positivo.
'''
def zwsolver ():
	res = []
	aux = 0
	three = int(input("Enter the power of the three:\n"))
	smooth = int(input("Enter the 3-smooth:\n"))
	if (smooth%3 == 1):
		beg = 2
	else:
		beg = 1
	for i in range(beg, 50, 2):
		aux = (2**i-smooth)/(3**three)
		if ((2**i-smooth)%(3**three) == 0):
			res.append([aux, i])
	print("two    starting number")
	for i in range(len(res)):
		aux = countdigs(res[i][1])
		print(res[i][1], end="")
		for j in range(7-aux):
			print(" ", end="")
		print(res[i][0])

def countOnes (num):
	count = 0
	aux = num
	while aux != 0:
		aux = aux & (aux-1)
		count += 1
	return count

def binToStr (num, digs):
	string = str(bin(num))[2:]
	top = digs-len(string)
	for i in range(top):
		string = "0" + string
	return string


def binaryGen (two, three):
	top = 2**(two+1)
	for i in range(top):
		if countOnes(i) == three:
			yield binToStr(i, two)

'''
This function takes an "a" value and finds all the other trios (w, x, z) that
can solve the equation.
Notes:
- With this fuction I found that, for the same value of "a", the greater the
difference a-w, the higher the number "x", with 2^a beeing the greater "x".
- It displays the details of the route encoded in a binary number, where 1 is
a double step of the kind odd-even (f(f(x)) = (3x+1)/2), and the 0 is the even
step (f(x) = x/2). The steps are read from the right to the left.
- At the end of the output, it shows a list with only the odd numbers from the
original output.

Essa função recebe um valor de "a" e acha todas as trincas (w, x, z) que
resolvem a equação.
Notas:
- Com essa função eu descobri que, para o mesmo valor de "a", quanto maior a
diferença a-w, maior o número "x", sendo o maior "x" o 2^a.
- A função mostra detalhes sobre a rota codificada em um número binário, onde
1 é um passo duplo do tipo ímpar par (f(f(x)) = (3x+1)/2), e o 0 é o passo par
(f(x) = x/2). Os passos são lidos da direita para a esquerda.
- Depois de imprimir todos as soluções, a função imprime uma lista somente com
as soluções ímpares da lista original.
'''
def asolver (plot=0, two=-1):
	if plot == 0:
		two = int(input("Enter the power of the two:\n")) - 1
	digits = [0, 0, 0]
	mem = []
	if plot == 0:
		print("power of three    inicial number    3-smooth    steps")
	for k in range(math.floor(2*two/3)+1):
		for i in binaryGen(two, k):
			res = 2
			con = 1
			for j in i:
				res = 2*res
				# print(res)
				if j == "1":
					res -= 1
					if res != 3 and res%3 == 0 and (res/3)%2 == 1:
						res /= 3
						# print(res)
					else:
						con = 0
						# print("break")
						break
			if con == 1:
				tsmooth = int(2**(two+1) - res*3**k)
				if plot == 0:
					digits[0] = countdigs(k)
					digits[1] = countdigs(int(res))
					digits[2] = countdigs(tsmooth)
					print(k, end="")
					for j in range(18-digits[0]):
						print(" ", end="")
					print(int(res), end="")
					for j in range(18-digits[1]):
						print(" ", end="")
					print(tsmooth, end="")
					for j in range(12-digits[2]):
						print(" ", end="")
					print("0"+i)
				if (res%2 == 1):
					mem.append([k, int(res), tsmooth, "0"+i])
	if plot == 0:
		print("================ Taking out the evens ================")
	else:
		print("================ two =", two+1, "================")
	print("power of three    inicial number    3-smooth    steps")
	for i in range(len(mem)):
		digits[0] = countdigs(mem[i][0])
		digits[1] = countdigs(mem[i][1])
		digits[2] = countdigs(mem[i][2])
		print(mem[i][0], end="")
		for j in range(18-digits[0]):
			print(" ", end="")
		print(mem[i][1], end="")
		for j in range(18-digits[1]):
			print(" ", end="")
		print(mem[i][2], end="")
		for j in range(12-digits[2]):
			print(" ", end="")
		print(mem[i][3])
	return mem

def plotasolver ():
	top = int(input("Enter the maximum power of two:\n"))
	colors = ['bo', 'ko', 'ro', 'co', 'yo']
	attcol = 0
	fig, ax = plt.subplots()
	for i in range(top):
		layer = asolver(1, i)
		j = 0
		qntt = len(layer)
		while j < qntt:
			attcol = 0
			plt.plot(layer[j][0], i, 'bo')
			while (j < qntt-1 and layer[j+1][0] == layer[j][0]):
				j += 1
				attcol = (attcol + 1)%5
				plt.plot(layer[j][0], i, colors[attcol])
			j += 1
	plt.xlabel("Three's power")
	plt.ylabel("Two's power")
	ax.grid(True)
	plt.tight_layout()
	plt.show()

def bmod (num, twos, three, mod):
	tpow = 2**mod
	aux = num%tpow
	tmod = math.ceil(math.log2(mod*lgt))
	tmod = 2**tmod
	top = len(twos)
	aux *= (((3**tmod)%tpow)**(top//tmod)*((3**(top%tmod))%tpow))%tpow
	i = top-1
	while i > three-1:
		aux = (aux + 2**twos[i]*((((3**tmod)%tpow)**(i//tmod)*((3**(i%tmod))%tpow))%tpow))%tpow
		i -= 1
	return aux

'''
This function gets as input the "x" and the "w" and finds the "z" and the "a"
values that solves the equation, using a different algorithm.

Explanation:
First, let z = sum[i from 0 to w-1](2^(b_i)*3^i), where all b_i are zero or
positive integers and b_(i-1) > b_i > b_(i+1). We know that the first term of
this summation is a power of two, and also that 2^(b_0) < 2^a, otherwise "x"
has to be a negative number.
So, to find the value of "z", we do:
x*3^w + z = 2^a    mod 2^p
p = 1 at the beginning
x*3^w + z = 0      mod 2    (We know that 2^a = 0 mod 2 because a > b_0)
When we do z mod 2, we are doing sum[i from 0 to w-1](2^(b_i)*3^i) mod 2.

We have two options to find z mod 2:
- If b_(w-1) = 0 = p-1, and we know that b_(w-n) > b_(w-1), for all n > 1, so
all the other terms are multiple of 2, except the last one, that is
2^b_(w-1)*3^(w-1) = 3^(w-1), and is odd. So z = 3^(w-1) = 1 mod 2.
- If b_(w-1) != 0, it can only be greater than 0, so we have that
b_(w-n) > b_(w-1), for all n > 1, so all the terms of the summation are 0 mod 2,
then z = 0 mod 2.

But how we know which option to choose?
Just take the value of x*3^w mod 2. If it's 1, so we have to have z = 1 mod 2,
so we discovered the last term of "z". If it's 0, so we have to have that
z = 0 mod 2, so we know that b_(w-1) != 0.

If we found the value of b_(w-1), the next step is:
x*3^w + 2^b_(w-1)*3^(w-1) + (z-2^b_(w-1)*3^(w-1)) = 2^a    mod 2^p
Increment "p" by one, now p = 2
x*3^w + 2^b_(w-1)*3^(w-1) + (z-2^b_(w-1)*3^(w-1)) = 0      mod 4

Else:
x*3^w + z = 2^a    mod 2^p
Increment "p" by one, now p = 2
x*3^w + z = 0      mod 4

So we keep doing this until we find the value of b_0, than we have the value of
"z". Now just do log2(x*3^w + z) to find the "a".

The sum x*3^w + z can be very large, so this function uses the "bmod" to
calculate the value of the modules.



Essa função recebe "x" e "w" como entrada e acha o "z" e o "a" que resolvem a
equação, usando um algoritmo diferente.

Explicação:
Primeiro, suponha z = sum[i from 0 to w-1](2^(b_i)*3^i), onde todos os b_i >= 0
e inteiros e b_(i-1) > b_i > b_(i+1). Nós sabemos que o primeiro termo dessa
soma é uma potência de dois, e também que 2^(b_0) < 2^a, caso contrário o "x"
teria que ser negativo.
Para achar o valor de "z", nós fazemos:
x*3^w + z = 2^a    mod 2^p
p = 1 no começo
x*3^w + z = 0      mod 2    (nós sabemos que 2^a = 0 mod 2 pois a > b_0)
Quando fazemos z mod 2, nós estamos fazendo sum[i from 0 to w-1](2^(b_i)*3^i) mod 2.

Temos duas opções para achar z mod 2:
- Se b_(w-1) = 0, então sabemos que b_(w-n) > b_(w-1), para qualquer n > 1,
então todos os outros termos são múltiplos de 2, exceto o último, que é
2^b_(w-1)*3^(w-1) = 3^(w-1), e é ímpar. Então z = 3^(w-1) = 1 mod 2.
- Se b_(w-1) != 0, ele só pode ser maior que 0, então temos b_(w-n) > b_(w-1),
para todo n > 1, então todos os termos da soma são iguais a 0 mod 2, então
z = 0 mod 2.

Mas como sabemos qual opção escolher?
É só acharmos o valor de x*3^w mod 2. Se for 1, então nós temos que z = 1 mod 2,
então descobrimos o último termo de "z". Se for 0, então temos que z = 0 mod 2,
então sabemos que b_(w-1) != 0.

Se achamos o valor de b_(w-1), então o próximo passo é:
x*3^w + 2^b_(w-1)*3^(w-1) + (z-2^b_(w-1)*3^(w-1)) = 2^a    mod 2^p
Aumentando "p" em um, agora p = 2
x*3^w + 2^b_(w-1)*3^(w-1) + (z-2^b_(w-1)*3^(w-1)) = 0      mod 4

Caso contrário:
x*3^w + z = 2^a    mod 2^p
Aumentando "p" em um, agora p = 2
x*3^w + z = 0      mod 4

Então continuamos a fazer isso até obter o valor de b_0, então temos o valor de
"z". Agora é só fazer log2(x*3^w + z) para achar o valor de "a".

Como a soma x*3^w + z pode ser muito grande, então essa função usa a "bmod" para
calcular os módulos.
'''
def xwsolver (massive=0, num=0, three=0):
	if massive == 0:
		num = int(input("Enter the inicial number:\n"))
		three = int(input("Enter the power of the three:\n"))
	aux = num
	mem = 0
	mod = 1
	a = 0
	twos = [0 for i in range(three)]
	firsttwos = 0
	summ = 0
	while (aux%2 == 0):
		aux /= 2
		firsttwos += 1
	while (three > 0):
		a = 0
		mem = bmod(aux, twos, three, mod)
		while (mem == 0):
			mod += 1
			mem = bmod(aux, twos, three, mod)
		three -= 1
		twos[three] = mod-1
		mod += 1
	for i in range(len(twos)):
		summ += (3**i)*(2**twos[i])
	tsmooth = int(summ*2**firsttwos)
	summ += aux*3**(len(twos))
	two = math.log2(summ)+firsttwos
	if massive == 0:
		print("- 3-smooth associated:", tsmooth)
		print("- Power of the two:   ", two)
	return two, tsmooth

'''
Continuous version of "xwsolver". It just start with a rational "w" and it's
less precise due to the overflow.

This is an attempt to make a continuous version, so it's not really the
continuous version.

Versão contínua do "xwsolver". A única diferença é que ela começa com um "w"
racional e não é tão precisa por causa do overflow.

Essa é uma tentativa de fazer uma versão contínua, portanto não é uma versão
contínua da verdade.
'''
def xwsolvertwo (massive=0, num=0, three=0):
	if massive == 0:
		num = int(input("Enter the inicial number:\n"))
		three = int(input("Enter the power of the three:\n"))
	fthree = three
	aux = num
	mod = 1
	firsttwos = 0
	summ = 0
	while (aux%2 == 0):
		aux /= 2
		firsttwos += 1
	summ = aux*3**three
	three -= 1
	while (three >= 0):
		while (summ%(2**mod) == 0):
			mod += 1
		summ += (3**three)*(2**(mod-1))
		mod += 1
		three -= 1
	two = math.log2(summ)+firsttwos
	tsmooth = 2**two - num*3**fthree
	if massive == 0:
		print("- 3-smooth associated:", tsmooth)
		print("- Power of the two:   ", two)
	return two, tsmooth

'''
This function executes the "xwsolver" algorithm to various values of "w".

Essa função executa o algoritmo da "xwsolver" para vários valores de "w".
'''
def xsolver (plot=0, freq=0, ver=0):
	num = int(input("Enter the inicial number:\n"))
	top = int(input("Enter the maximum power of the three:\n"))
	if plot == 0 and freq == 0:
		freq = 10**(int(input("Enter the number of points per unit as a power of ten (eg: enter 2 for 100ppu):\n")))
	ret = []
	realtwo = -1
	realthree = 0
	digits = [0, 0]
	if plot == 0:
		print("three    two                   3-smooth")
	for i in range(top*freq+1):
		three = i/freq
		if ver == 0:
			two, tsmooth = xwsolver(1, num, int(three))
		else:
			two, tsmooth = xwsolvertwo(1, num, three)
		if (two%1 == 0 and realtwo == -1):
			realtwo = two
			realthree = three
		if plot == 0:
			digits[0] = countdigs(three)
			digits[1] = countdigs(two)
			print(three, end="")
			for j in range(9-digits[0]):
				print(" ", end="")
			print(two, end="")
			for j in range(22-digits[1]):
				print(" ", end="")
			print(tsmooth)
		ret.append([three, two])
	return top, realthree, realtwo, ret

'''
This function plots the pairs (w, a) returned from the function "xsolver".

Essa função plota os pares (w, a) obtidos por meio da função "xsolver".
'''
def plotxsolver (ver=0):
	if ver == 0:
		top, three, two, pts = xsolver(1, 1, 0)
	else:
		top, three, two, pts = xsolver(1, 100, 1)
	fig, ax = plt.subplots()
	first = pts[0][1]
	plt.plot([0, top], [-2*three+two, 2*(top-three)+two], 'b-')
	for i in range(len(pts)-1):
		plt.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]], 'k-')
		if (pts[i][0]%1 == 0 and pts[i][1]%1 == 0):
			plt.plot(pts[i][0], pts[i][1], 'ro')
	if (pts[len(pts)-1][0]%1 == 0 and pts[len(pts)-1][1]%1 == 0):
		plt.plot(pts[len(pts)-1][0], pts[len(pts)-1][1], 'ro')
	plt.plot([0, top], [first, fgr*top+first], 'y-')
	plt.xlabel("Three's power")
	plt.ylabel("Two's power")
	ax.grid(True)
	plt.tight_layout()
	plt.show()

def xasolver ():
	num = int(input("Enter the inicial number:\n"))
	two = int(input("Enter the power of the two:\n"))
	top = int(input("Enter the maximum 3-smooth:\n"))
	if (top > 2**two):
		top = 2**two
	print("3-smooth        three")
	for i in range(top):
		three = math.log((2**two-i)/num, 3)
		#if three%1 == 0:
		print(i, end="")
		for j in range(16-countdigs(i)):
			print(" ", end="")
		print(three)

def main ():
	print("What function do you want to use?")
	print("  - collatz (c)")
	print("  - 3-smooth finder (t)")
	print("  - zw-solver (z)")
	print("  - a-solver (a)")
	print("  - x-solver (x)")
	print("  - xa-solver (xa)")
	sel = input()
	if sel == "c":
		sel = input("Unitary (u) or massive (m)?\n")
		if sel == "u":
			collatz(-1)
		elif sel == "m":
			mcollatz()
		else:
			print("Invalid input, quiting the program.....")
	elif sel == "t":
		tsmooth()
	elif sel == "z":
		zwsolver()
	elif sel == "a":
		sel = input("Plot (y/n)?\n")
		if sel == "y":
			plotasolver()
		elif sel == "n":
			asolver()
		else:
			print("Invalid input, quiting the program.....")
	elif sel == "x":
		print("What sub-function do you want to use?")
		print("  - solve using the three value (w)")
		print("  - solve discretely ('always' stable) (d)")
		print("  - solve continuously (stable to three < 25) (c)")
		print("  - solve discretely and plot the result ('always' stable) (dp)")
		print("  - solve continuously and plot the result (stable to three < 25) (cp)")
		sel = input()
		if sel == "w":
			xwsolvertwo()
		elif sel == "d":
			xsolver(0, 1)
		elif sel == "c":
			xsolver(0, 0, 1)
		elif sel == "dp":
			plotxsolver()
		elif sel == "cp":
			plotxsolver(1)
		else:
			print("Invalid input, quiting the program.....")
	elif sel == "xa":
		xasolver()
	else:
		print("Invalid input, quiting the program.....")

if __name__ == "__main__":
	main()
