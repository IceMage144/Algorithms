## Evo

### Purpose

Develop a simple program using neural networks and genetic algorithm

### What it does

This program simulates a competition between shooting balls. The actions of
the balls are defined by three neural networks, one for deciding if the ball
will walk or not, one for defining its turning velocity and the third for
defining the shooting speed. After winning a round, the weights of the neural
networks of the winner are changed by a random ammount, giving the illusion of
a mutation. The competition starts with 32 balls.

### How to use

Just run `python evo.py` at the command line and watch the balls fight.
![evo print](/evo.png)
