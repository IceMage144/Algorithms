'''
This program was made to solve a puzzle called "celtic knot", from the game
runescape (http://runescape.wikia.com/wiki/Treasure_Trails/Guide/Celtic_knots).

Esse programa foi feito para resolver um quebra-cabeça chamado "nó celta", do
jogo runescape (http://runescape.wikia.com/wiki/Treasure_Trails/Guide/Celtic_knots).
'''


def checkBoard(bb, rb, wb, blue, red, white, knots):
	if knots == 6:
		if (blue[bb] == white[(wb+6)%16] and blue[(bb+6)%16] == white[wb] and white[(wb+1)%16] == red[(rb+5)%16] and white[(wb+5)%16] == red[(rb+1)%16] and blue[(bb+8)%16] == red[(rb+6)%16] and blue[(bb+14)%16] == red[rb]):
			return 1
	if knots == 8:
		comp1 = (blue[bb] == white[(wb+12)%16] and blue[(bb+2)%16] == white[wb] and blue[(bb+7)%16] == white[(wb+1)%16] and blue[(bb+9)%16] == white[(wb+11)%16])
		comp2 = (white[(wb+8)%16] == red[(rb+11)%16] and white[(wb+4)%16] == red[(rb+9)%16] and white[(wb+3)%16] == red[(rb+2)%16] and white[(wb+9)%16] == red[rb])
		if (comp1 and comp2):
			return 1
	return 0

def specialprint(array, beg):
	aux = beg
	end = (beg+15)%16
	while aux != end:
		print(array[aux], end=" ")
		aux = (aux+1)%16
	print(array[aux])
	return 0

def solve (knots, blue, red, white):
	bb = 0
	rb = 0
	wb = 0
	done = 0
	if knots == 6:
		while (done == 0 and rb < 16 and wb < 16):
			rb = 0
			while ((blue[bb] != white[(wb+6)%16] or blue[(bb+6)%16] != white[wb]) and wb < 16):
				bb += 1
				if bb == 16:
					wb += 1
					bb = 0
			while ((white[(wb+1)%16] != red[(rb+5)%16] or white[(wb+5)%16] != red[(rb+1)%16] or blue[(bb+8)%16] != red[(rb+6)%16] or blue[(bb+14)%16] != red[rb]) and rb < 16):
				rb += 1
			done = checkBoard(bb, rb, wb, blue, red, white, knots)
		if done:
			print("====================================================")
			specialprint(blue, (bb+15)%16)
			specialprint(red, (rb+15)%16)
			specialprint(white, (wb+7)%16)
			return 1
	if knots == 8:
		while (done == 0 and rb < 16 and wb < 16):
			rb = 0
			while ((blue[bb] != white[(wb+12)%16] or blue[(bb+2)%16] != white[wb] or blue[(bb+7)%16] != white[(wb+1)%16] or blue[(bb+9)%16] != white[(wb+11)%16]) and wb < 16):
				bb += 1
				if bb == 16:
					wb += 1
					bb = 0
			while ((white[(wb+8)%16] != red[(rb+11)%16] or white[(wb+4)%16] != red[(rb+9)%16] or white[(wb+3)%16] != red[(rb+2)%16] or white[(wb+9)%16] != red[rb]) and rb < 16):
				rb += 1
			done = checkBoard(bb, rb, wb, blue, red, white, knots)
		if done:
			print("====================================================")
			specialprint(blue, (bb+14)%16)
			specialprint(red, (rb+14)%16)
			specialprint(white, (wb+13)%16)
			return 1
	else:
		print("The solver still doesn't support 10 and 12 knots puzzle")
		return 0
	print("Wrong input. The puzzle doesn\'t have a solution.")
	return 0

def main ():
	puzz = int(input("How many knots does the puzzle have?\n"))
	while (puzz != 6 and puzz != 8 and puzz != 10 and puzz != 12):
		puzz = int(input("This kind of puzzle does not exists. Check again\n"))
	print("Input the blue, red and white strips, respectively, begining with the upmost rune and rotating clockwise.")
	print("Input the runes at the same strip at the same line, separated with spaces and divide the strips with line end.")
	print("You can use any visible character to represent each rune, remembering that you can use more than one character and uppercase is different from downcase")
	blue = input().split()
	red = input().split()
	white = input().split()
	print("solving...")
	solve(puzz, blue, red, white)

main()
