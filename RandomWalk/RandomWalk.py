import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, FuncAnimation
from random import random
import sys

dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))

class Walker:
    POS = [0, 0]
    MAXX = 0
    MAXY = 0

    def __init__(self, maxX, maxY):
        #ind = round(random())
        #if (random() < 0.5):
        #    self.POS = [ind*maxX, int(random()*maxY)]
        #else:
        #    self.POS = [int(random()*maxX), ind*maxY]
        self.POS = [int(random()*maxX), int(random()*maxY)]
        self.MAXX = maxX
        self.MAXY = maxY

    def walk(self):
        rand = int(4*random())
        self.POS[0] = max(0, min(self.MAXX-1, dirs[rand][0]+self.POS[0]))
        self.POS[1] = max(0, min(self.MAXY-1, dirs[rand][1]+self.POS[1]))
        return self.POS[0], self.POS[1]

def main():
    try:
        f = open(sys.argv[1])
        wkrs = int(sys.argv[2])
    except IndexError:
        print("Usage: RandomWalk <file with initial seed> <number of walkers>")
    got = False
    mat = []
    maxX = 0
    maxY = 0
    immat = []
    for line in f:
        vec = [int(s) for s in line.split(" ")]
        if not got:
            maxX = int(vec[0])
            maxY = int(vec[1])
            got = True
            mat = [[0 for j in range(maxY)] for i in range(maxX)]
        else:
            mat[vec[0]][vec[1]] = 1
    f.close()
    fig, ax = plt.subplots(figsize=(5, 5))
    c = ax.imshow(mat, interpolation='nearest',
                            origin='bottom',
                            aspect='auto', # get rid of this to have equal aspect
                            cmap='Blues')
    wal = [Walker(maxX, maxY) for i in range(wkrs)]
    timeText = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    def update():
        immat = [v.copy() for v in mat]
        for j in range(len(wal)):
            newX, newY = wal[j].walk()
            immat[newX][newY] = 0.5
            for d in dirs:
                x = max(0, min(maxX-1, newX+d[0]))
                y = max(0, min(maxY-1, newY+d[1]))
                if mat[x][y] == 1:
                    mat[newX][newY] = 1
                    wal[j] = Walker(maxX, maxY)
        yield immat

    # function that plot each frame
    def plot(update):
        screen = update
        c.set_data(screen)
        #timeText.set_text(f"Time = {time}")
        return c
    # create animation
    ani = FuncAnimation(fig, plot, update, interval=10)
    plt.xlim(0, maxX)
    plt.ylim(0, maxY)
    #plt.axis('off')
    plt.show()

main()
