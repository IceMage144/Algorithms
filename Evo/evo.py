import pygame
import random
import math
import time
import numpy as np
import copy
import bisect

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
BLUE = (127, 127, 255)
RED = (255, 64, 64)
GREEN = (64, 255, 64)

def roundNpArr(arr):
    r = []
    for i in arr:
        r.append(int(round(i)))
    return np.array(r)

def mod(x, y):
    if x < 0:
        return -((-x)%y)
    return x%y

def stdAng(x):
    tau = 2*math.pi
    x = mod(x, tau)
    if x > math.pi:
        x -= tau
    elif x < -math.pi:
        x += tau
    return x

def fastGetAngle(dx, dy):
    cos = dx/math.sqrt(dx*dx + dy*dy)
    x = -cos if (cos > 0) else cos
    if x < -0.5:
        x += 1
        ang = math.pi - math.sqrt(2*x)*(1 + x/12*(1 + 0.225*x))
    else:
        sqx = x*x
        ang = math.pi/2 - x*(1 + sqx*(1/6 + 0.075*sqx))
    if cos > 0:
        ang = math.pi - ang
    if dy < 0:
        ang = -ang
    return ang


def polVec(theta, mu):
    return (math.cos(theta)*mu, -math.sin(theta)*mu)

def clampCircle(center, rad, rect):
    center[0] = min(max(center[0], rect.left + rad), rect.right - rad)
    center[1] = min(max(center[1], rect.top + rad), rect.bottom - rad)

def teleport(center, rect):
    m = min(max(center[0], rect.left), rect.right)
    if m == rect.left:
        center[0] = rect.right
    elif m == rect.right:
        center[0] = rect.left
    else:
        center[0] = m
    m = min(max(center[1], rect.top), rect.bottom)
    if m == rect.top:
        center[1] = rect.bottom
    elif m == rect.bottom:
        center[1] = rect.top
    else:
        center[1] = m

def point_circleCollide(p, center, rad):
    xdif = p[0] - center[0]
    ydif = p[1] - center[1]
    return (xdif*xdif + ydif*ydif < rad*rad)

def point_semi_circleCollide(p, center, rad, iniAng, finAng):
    iniAng = stdAng(iniAng)
    finAng = stdAng(finAng)
    xdif = p[0]-center[0]
    ydif = center[1]-p[1]
    ang = fastGetAngle(xdif, ydif)
    dSq = xdif*xdif + ydif*ydif
    if dSq < rad*rad and ang > iniAng and ang < finAng:
        return True
    return False

def circleCollide(center1, rad1, center2, rad2):
    xdif = center1[0] - center2[0]
    ydif = center1[1] - center2[1]
    s = rad1 + rad2
    return (xdif*xdif + ydif*ydif < s*s)

def distSq(p1, p2):
    xdif = p1[0]-p2[0]
    ydif = p1[1]-p2[1]
    return xdif*xdif + ydif*ydif

def dist(p1, p2):
    xdif = p1[0]-p2[0]
    ydif = p1[1]-p2[1]
    return math.sqrt(xdif*xdif + ydif*ydif)

# Neural network class for thinking
class Network(object):
    TH = 0.2
    def __init__(self, numNeurons):
        self.numNeurons = numNeurons
        self.weights = []
        self.bias = []
        self.total = 0
        self.wCum = [0]
        self.bCum = [0]
        for i in range(len(numNeurons) - 1):
            self.weights.append(np.random.rand(numNeurons[i], numNeurons[i+1])*2 - 1)
            self.bias.append(np.random.rand(numNeurons[i+1])*2 - 1)
            self.wCum.append(numNeurons[i]*numNeurons[i+1])
            self.bCum.append(numNeurons[i+1])
            self.total += (numNeurons[i] + 1)*numNeurons[i+1]
        self.wCum = np.cumsum(self.wCum)
        self.bCum = np.cumsum(self.bCum) + self.wCum[len(self.wCum)-1]

    def sigmoid(x):
        return 1/(1 + np.exp(-x))

    def fProp(self, inp):
        hVals = inp
        for i in range(len(self.weights)):
            hVals = Network.sigmoid(np.dot(hVals, self.weights[i]) + self.bias[i])
        return hVals

    def mutate(self, p):
        for i in sorted(random.sample(range(0, self.total), math.floor(p*self.total))):
            b = bisect.bisect(self.wCum, i)
            if b != len(self.wCum):
                k = i - self.wCum[b-1]
                s = self.weights[b-1].shape
                self.weights[b-1][k//s[1]][k%s[1]] += Network.TH*(2*random.random() - 1)
            else:
                b = bisect.bisect(self.bCum, i)
                k = i - self.bCum[b-1]
                self.bias[b-1][k] += Network.TH*(2*random.random() - 1)

    def copy(self):
        return copy.deepcopy(self)

# Entity base class
class Entity(object):
    LIST = {}
    IDCOUNTER = 0
    def __init__(self):
        self.id = Entity.IDCOUNTER
        Entity.LIST[self.id] = self
        Entity.IDCOUNTER += 1

    def die(self):
        if self.id in Entity.LIST:
            Entity.LIST.pop(self.id)

    def update(screen, t):
        it = dict(Entity.LIST)
        for _, e in it.items():
            e.update(screen, t)

    def draw(screen):
        it = dict(Entity.LIST)
        for _, e in it.items():
            e.draw(screen)

    def remove(self):
        if Entity.LIST.get(self.id):
            Entity.LIST.pop(self.id)

    def add(self):
        if not Entity.LIST.get(self.id):
            Entity.LIST[self.id] = self

# Circlet class for conquering
class Circlet(Entity):
    LIST = {}
    def __init__(self, x, y):
        super().__init__()
        Circlet.LIST[self.id] = self
        self.life = 100
        self.angle = math.pi*(2*random.random() - 1)
        self.moving = False
        self.pos = np.array([x, y])
        self.turnSpeed = 0
        self.range = 120
        self.visAngle = 0.5
        self.energy = 0
        self.rad = 10
        self.speed = 0.2
        self.shootNN = Network([28, 14, 5, 1])
        self.moveNN = Network([28, 14, 5, 1])
        self.turnNN = Network([28, 14, 5, 1])
        self.points = 0.6
        self.shootTime = 200
        self.nextShoot = 0
        self.color = [255, 255, 255]
        self.feed = [0.0]*28
        self.active = True

    def draw(self, screen):
        rpos = roundNpArr(self.pos)
        pygame.draw.lines(screen, GRAY, True, [rpos + polVec(self.angle-self.visAngle, self.range),
                                                rpos,
                                                rpos + polVec(self.angle+self.visAngle, self.range)], 1)
        pygame.draw.circle(screen, self.color, rpos, self.rad)

    def update(self, screen, t):
        for i in range(len(self.feed)):
            self.feed[i] = 0
        iniAng = stdAng(self.angle-self.visAngle)
        finAng = stdAng(self.angle+self.visAngle)

        # Check collision and vision of energies
        it = dict(Energy.LIST)
        for i, e in it.items():
            xdif = e.pos[0] - self.pos[0]
            ydif = self.pos[1] - e.pos[1]
            distSq = xdif**2 + ydif**2
            if distSq < (e.rad + self.rad)**2 and Energy.LIST.get(i):
                e.die()
                self.gainEnergy(5)
            elif distSq < self.range**2 and Energy.LIST.get(i):
                ang = fastGetAngle(xdif, ydif)
                if iniAng <= finAng and ang > iniAng and ang < finAng:
                    num = math.floor(abs(8*(ang - iniAng)/(2*self.visAngle)))
                    self.feed[num] = 1
                elif iniAng > finAng:
                    if ang > iniAng:
                        num = math.floor(abs(8*(ang - iniAng)/(2*self.visAngle)))
                        self.feed[num] = 1
                    elif ang < finAng:
                        num = math.floor(abs(8*(ang - iniAng + 2*math.pi)/(2*self.visAngle)))
                        self.feed[num] = 1

        # Check collision and vision of bullets
        it = dict(Bullet.LIST)
        for i, e in it.items():
            xdif = e.pos[0] - self.pos[0]
            ydif = self.pos[1] - e.pos[1]
            distSq = xdif**2 + ydif**2
            if distSq < (e.rad + self.rad)**2 and Bullet.LIST.get(i):
                e.die()
                self.life -= 30
                if self.life <= 0:
                    self.die()
                    e.owner.gainEnergy(5)
                    return
            elif e.owner != self and distSq < self.range**2 and Bullet.LIST.get(i):
                ang = fastGetAngle(xdif, ydif)
                if iniAng <= finAng and ang > iniAng and ang < finAng:
                    num = math.floor(abs(8*(ang - iniAng)/(2*self.visAngle)))
                    self.feed[num+8] = 1
                elif iniAng > finAng:
                    if ang > iniAng:
                        num = math.floor(abs(8*(ang - iniAng)/(2*self.visAngle)))
                        self.feed[num+8] = 1
                    elif ang < finAng:
                        num = math.floor(abs(8*(ang - iniAng + 2*math.pi)/(2*self.visAngle)))
                        self.feed[num+8] = 1

        # Check vision of enemies
        it = dict(Circlet.LIST)
        for i, e in it.items():
            xdif = e.pos[0] - self.pos[0]
            ydif = self.pos[1] - e.pos[1]
            distSq = xdif**2 + ydif**2
            if e != self and distSq < self.range**2 and Circlet.LIST.get(i):
                ang = fastGetAngle(xdif, ydif)
                if iniAng <= finAng and ang > iniAng and ang < finAng:
                    num = math.floor(abs(8*(ang - iniAng)/(2*self.visAngle)))
                    self.feed[num+16] = 1
                elif iniAng > finAng:
                    if ang > iniAng:
                        num = math.floor(abs(8*(ang - iniAng)/(2*self.visAngle)))
                        self.feed[num+16] = 1
                    elif ang < finAng:
                        num = math.floor(abs(8*(ang - iniAng + 2*math.pi)/(2*self.visAngle)))
                        self.feed[num+16] = 1

        #print(self.feed)

        # Add more information to feed vector
        self.feed[24] = self.life/100
        self.feed[25] = self.pos[0]/screen.get_rect().width
        self.feed[26] = self.pos[1]/screen.get_rect().height
        self.feed[27] = (self.angle + math.pi)/(2*math.pi)

        # Think
        mr = self.moveNN.fProp(self.feed)[0]
        sr = self.shootNN.fProp(self.feed)[0]
        tr = self.turnNN.fProp(self.feed)[0]

        # Red is the shooting frequence, green is the turning speed and blue is the hyperativity
        self.color = [0 if (sr > 0.8) else 255*(0.8-sr)/0.8,
                      0 if (tr > 0.4 and tr < 0.6) else 255*(math.fabs(tr-0.5)-0.1)/0.4,
                      0 if (mr <= 0.2) else 255*(mr-0.2)/0.8]

        # Aplying outputs
        self.moving = (mr > 0.2)
        self.shootTime = math.inf if (sr > 0.8) else sr*1000 + 100
        self.turnSpeed = 0 if (tr > 0.4 and tr < 0.6) else (tr - 0.5)/100
        self.angle += self.turnSpeed
        if self.moving:
            self.pos += polVec(self.angle, self.speed)
        teleport(self.pos, screen.get_rect())
        #if self.energy >= 20:
        #    self.multiply(screen)
        #    self.energy -= 20
        self.nextShoot += 1
        if self.shootTime <= self.nextShoot:
            self.shoot()
            self.nextShoot = 0
        if not self.active:
            self.remove()

    def multiply(self, screen):
        rect = screen.get_rect()
        c = Circlet(rect.width*random.random(), rect.height*random.random())
        c.shootNN = self.shootNN.copy()
        c.moveNN = self.moveNN.copy()
        c.turnNN = self.turnNN.copy()
        c.mutate(0.2)
        #self.mutate(0.2)
        return c

    def mutate(self, p):
        self.shootNN.mutate(p)
        self.moveNN.mutate(p)
        self.turnNN.mutate(p)

    def shoot(self):
        m = self.pos + polVec(self.angle, self.rad + 6)
        Bullet(m[0], m[1], self.angle, self)

    def gainEnergy(self, qtd):
        self.energy += qtd
        self.life = min(self.life + qtd, 100)

    def die(self):
        super().die()
        if Circlet.LIST.get(self.id):
            Circlet.LIST.pop(self.id)

    def remove(self):
        super().remove()
        if Circlet.LIST.get(self.id):
            Circlet.LIST.pop(self.id)
        self.active = False

    def add(self):
        super().add()
        if not Circlet.LIST.get(self.id):
            Circlet.LIST[self.id] = self
        self.active = True

    def reset(self):
        self.life = 100
        self.energy = 0
        self.angle = math.pi*(2*random.random() - 1)
        self.moving = False
        self.turnSpeed = 0

    def __str__(self):
        return str(self.id)

# Energy class for reproducing
class Energy(Entity):
    LIST = {}
    def __init__(self, x, y):
        super().__init__()
        Energy.LIST[self.id] = self
        self.pos = np.array([x, y])
        self.rad = 5
        self.points = 0.3

    def draw(self, screen):
        rpos = roundNpArr(self.pos)
        pygame.draw.circle(screen, BLUE, rpos, self.rad)

    def update(self, screen, t):
        pass

    def die(self):
        super().die()
        if self.id in Energy.LIST:
            Energy.LIST.pop(self.id)

# Bullet class for killing
class Bullet(Entity):
    LIST = {}
    DISTLIMIT = 500
    def __init__(self, x, y, ang, own):
        super().__init__()
        Bullet.LIST[self.id] = self
        self.pos = np.array([x, y])
        self.angle = ang
        self.rad = 5
        self.points = 1
        self.owner = own
        self.t = 0
        self.speed = 0.4

    def draw(self, screen):
        rpos = roundNpArr(self.pos)
        pygame.draw.circle(screen, RED, rpos, self.rad)

    def update(self, screen, t):
        self.pos += polVec(self.angle, self.speed)
        if self.t*self.speed > 500:
            self.die()
        teleport(self.pos, screen.get_rect())
        self.t += 1

    def die(self):
        super().die()
        if self.id in Bullet.LIST:
            Bullet.LIST.pop(self.id)

# Dummy class for testing
class Dummy(Circlet):
    def __init__(self):
        super().__init__(100, 100)

    def update(self, screen, t):
        self.pos = np.array(pygame.mouse.get_pos())

class Point(Entity):
    def __init__(self, x, y, color):
        super().__init__()
        self.pos = np.array([x, y])
        self.rad = 3
        self.color = color

    def draw(self, screen):
        rpos = roundNpArr(self.pos)
        pygame.draw.circle(screen, self.color, rpos, self.rad)

    def update(self, screen, t):
        pass

def checkVictory(battle, t, fps):
    if not Circlet.LIST.get(battle[0].id):
        return battle[1]
    if not Circlet.LIST.get(battle[1].id):
        return battle[0]
    if t > fps*60:
        if battle[0].life > battle[1].life:
            return battle[0]
        if battle[0].life < battle[1].life:
            return battle[1]
        if battle[0].energy > battle[1].energy:
            return battle[0]
        if battle[0].energy < battle[1].energy:
            return battle[1]
        return battle[random.randrange(2)]
    return None

def main():
    (width, height) = (1000, 600)
    pygame.display.set_caption('Evo')
    screen = pygame.display.set_mode((width, height))
    running = True
    bg = screen.get_rect()
    t = 0
    fps = 500.0
    draw = True
    clock = pygame.time.Clock()

    gen = 1
    power = 5 # Cannot be less than 3
    numCirclets = 2**power
    l = []
    nl = []
    for i in range(numCirclets):
        l.append(Circlet(width*random.random(), height*random.random()))
        l[i].remove()
    battle = [l.pop(), l.pop()]
    battle[0].add()
    battle[1].add()
    print("Generation 1")

    # Spawn initial circlets
    #for i in range(15):
    #    Circlet(width*random.random(), height*random.random())

    #for i in range(-100, 100, 1):
    #    Point(i+100, 100*np.arccos(math.cos(i*math.pi/100))+300, GREEN)
    #    Point(i+100, 100*fastGetAngle(math.cos(i*math.pi/100), math.sin(i*math.pi/100))+300, RED)

    #Circlet(width/2, height/2)
    #Dummy()

    # Main loop
    while running:
        # Handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    draw = (not draw)

        pygame.draw.rect(screen, BLACK, bg) # Clear window
        Entity.update(screen, t) # Update entities
        if draw:
            Entity.draw(screen) # Draw entities

        # Restore population
        #if len(Circlet.LIST) <= 3:
        #    it = dict(Circlet.LIST)
        #    for _, e in it.items():
        #        for j in range(5):
        #            e.multiply(screen)

        c = checkVictory(battle, t, fps)
        if c:
            for i, e in dict(Energy.LIST).items():
                e.die()
            for i, e in dict(Bullet.LIST).items():
                e.die()
            battle[0].remove()
            battle[1].remove()
            if c == battle[0]:
                battle[1].die()
            else:
                battle[0].die()
            c.reset()
            nl.append(c)
            if len(l) == 0:
                l = nl
                nl = []
            if len(l) == 4 and len(nl) == 0:
                d = power - 2
                m = list(l)
                for e in m:
                    for i in range(2**d):
                        c = e.multiply(screen)
                        c.remove()
                        l.append(c)
                random.shuffle(l)
                gen += 1
                print("Generation", gen)
            battle[0] = l.pop()
            battle[1] = l.pop()
            battle[0].add()
            battle[1].add()
            print(l)
            print(nl)
            t = 0

        # Spawn energy
        if t%(fps*2) == 0:
            Energy(random.randrange(bg.left, bg.right), random.randrange(bg.top, bg.bottom))

        pygame.display.flip()
        clock.tick(fps)
        t += 1

if __name__ == '__main__':
    main()
