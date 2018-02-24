import matplotlib.pyplot as plt
import matplotlib.patches as pat
from matplotlib.animation import FuncAnimation
from math import *
import numpy as np

tau = 2*pi

def frame(mod, factor):
    f, ax = plt.subplots(figsize=(5, 5))
    for i, j in zip(range(mod), np.arange(0, factor*mod, factor)):
        plt.plot([cos(tau*i/mod), cos(tau*(j%mod)/mod)], [sin(tau*i/mod), sin(tau*(j%mod)/mod)], "r-")
    circ = pat.Circle([0, 0], radius=1, fc="none", ec="k")
    ax.add_patch(circ)
    modText = ax.text(0, 1, f"Modulus: {mod}", transform=ax.transAxes)
    facText = ax.text(0, 0.95, f"Factor: {factor}", transform=ax.transAxes)
    plt.axis('equal')
    plt.axis('off')
    plt.show()

def animate(mod, step):
    lines = []
    pts = []
    f, ax = plt.subplots(figsize=(5, 5))
    circ = pat.Circle([0, 0], radius=1, fc="none", ec="k")
    ax.add_patch(circ)
    modText = ax.text(0, 1, f"Modulus: {mod}", transform=ax.transAxes)
    facText = ax.text(0, 0.95, "", transform=ax.transAxes)
    for i in range(mod):
        pts.append([cos(tau*i/mod), sin(tau*i/mod)])
        lines.append(ax.plot([pts[i][0], pts[i][0]], [pts[i][1], pts[i][1]], "r-")[0])
    def update():
        for factor in np.arange(step, mod, step):
            for i, j in zip(range(mod), np.arange(0, factor*mod, factor)):
                lines[i].set_xdata([pts[i][0], cos(tau*(j%mod)/mod)])
                lines[i].set_ydata([pts[i][1], sin(tau*(j%mod)/mod)])
            facText.set_text(f"Factor: {round(factor, 2)}")
            yield lines
    def plot(update):
        for line in lines:
            yield line
        yield facText
    ani = FuncAnimation(f, plot, update, interval=1000*step)
    plt.axis('equal')
    plt.axis('off')
    #ani.save("factor_anim.mp4")
    plt.show()

if __name__ == "__main__":
    print("Select a mode:")
    print("    - Show just a frame (f or 1)")
    print("    - Show an animation (a or 2)")
    mode = input()
    if mode == "f" or mode == "1":
        mod = int(input("Input the modulus:\n"))
        factor = float(input("Input the factor:\n"))
        frame(mod, factor)
    elif mode == "a" or mode == "2":
        mod = int(input("Input the modulus:\n"))
        step = float(input("Input the step:\n"))
        animate(mod, step)
