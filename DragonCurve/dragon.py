import turtle as ttl
import random

def drawDragonStep(t, par, depth, md, dir):
    if depth == md:
        t.pencolor(random.random(), random.random(), random.random())
        t.setheading((3-dir)*90)
        t.forward(1)
    else:
        if par:
            drawDragonStep(t, par, depth+1, md, dir)
            drawDragonStep(t, not par, depth+1, md, (dir+1)%4)
        else:
            drawDragonStep(t, not par, depth+1, md, (dir+1)%4)
            drawDragonStep(t, par, depth+1, md, dir)


def drawDragon(t, md):
    drawDragonStep(t, True, 0, md, 0)

def main():
    wn = ttl.Screen()
    ttl.tracer(0, 0)
    t = ttl.Turtle()
    t.penup()
    t.goto(150, 100)
    t.pendown()
    t.speed(0)
    drawDragon(t, 15)
    ttl.update()
    wn.exitonclick()

if __name__ == '__main__':
    main()
