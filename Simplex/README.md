## Simplex

### Purpose

Train to implement the simplex algorithm after seeing it at
[MAC0315 (Linear programming)](https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=MAC0315&verdis=3)
classes.

### What it does

The simplex.py file implements the simplex algorithm in a very silly way.
The revised_simplex.py implements the revised version of the simplex with
linear algebra, it's simpler and cleaner, but can't solve some systems.

### How to use

The input structure is a little different for simplex and revised_simplex.
If you want to solve the system

<a href="https://www.codecogs.com/eqnedit.php?latex=\begin{align*}&space;max\quad&space;&&space;mx&space;&plus;&space;ny&space;&plus;&space;pz\\&space;subject\text{&space;}to\quad&space;&&space;ax&space;&plus;&space;by&space;&plus;&space;cz&space;\leqslant&space;d\\&space;&&space;ex&space;&plus;&space;fy&space;&plus;&space;gz&space;\geqslant&space;h&space;\end{align*}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\begin{align*}&space;max\quad&space;&&space;mx&space;&plus;&space;ny&space;&plus;&space;pz\\&space;subject\text{&space;}to\quad&space;&&space;ax&space;&plus;&space;by&space;&plus;&space;cz&space;\leqslant&space;d\\&space;&&space;ex&space;&plus;&space;fy&space;&plus;&space;gz&space;\geqslant&space;h&space;\end{align*}" title="\begin{align*} max\quad & mx + ny + pz\\ subject\text{ }to\quad & ax + by + cz \leqslant d\\ & ex + fy + gz \geqslant h \end{align*}" /></a>

at simplex.py you should input (the first numbers are the number of varables and
the number of inequalities, respectively):

3 2

a b c -d

-e -f -g h

m n p 0

and at revised_simplex.py you should input:

3 2

a b c d

-e -f -g -h

m n p

To run the program just use the command `python simplex.py` or
`python revised_simplex.py` and input the formated inequalities.
This comes with the files in.txt and in2.txt that can be used as input
for simplex.py and revised_simplex.py respectively.
