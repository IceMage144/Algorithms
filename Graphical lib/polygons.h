#ifndef __POLYGONS_H__
#define __POLYGONS_H__

#include <iostream>
#include <cmath>

#define TAU 6.2831853

double sq (double x);

/*
Point struct:
Stores an 2D point.
	- Constructor:
		- Can be created without parameters (in this case the coordinates will
be (0,0)) or created with the x and y doubles (in this case the coordinates
will be (x,y))

Estrutura Point:
Guarda um ponto em 2 dimensões.
	- Construtor:
		- Pode ser criado sem parâmetros (nesse caso as coordenadas serão (0,0))
ou criado com os parâmetros x e y (nesse caso as coordenadas serão (x,y))
*/
struct Point {
	double x, y;
	Point (): x(0), y(0) {}
	Point (double x, double y): x(x), y(y) {}
};

/*
Rect struct:
Stores two oposite corners of a rectangle.
	- Constructor:
		- Can be created without parameters (in this case the corners will
be both (0,0)) or created with the urc (from upper right corner) and llc
(from lower left corner) points (in this case the corners will be these points)

Estrutura Rect:
Guarda os dois vértices opostos de um retângulo.
	- Construtor:
		- Pode ser criado sem parâmetros (nesse caso os vértices serão (0,0) e
(0,0)) ou criado fornecendo os pontos urc (de vétice superior direito em inglês)
e llc (de vértice inferior esquerdo em inglês) (nesse caso os vértices serão
esses pontos)
*/
struct Rect {
	Point urc, llc;
	Rect (): urc(Point(0, 0)), llc(Point(0, 0)) {}
	Rect (Point urc, Point llc): urc(urc), llc(llc) {}
};

/*
GraphicalObject class:
It's a pure virtual class that is the parent of all other graphical objects.
	- Destructor:
		- It's the standard C++ destructor. Used for all children classes.
	- has_point:
		- Input:
			- p: A point.
		- Output:
			- Outputs True if the GraphicalObject contains the point or False
otherwise.
	- boundingBox:
		- Output:
			- Outputs a Rect struct with the smaller rectangle that contains all
GraphicalObject's points.
	- clone:
		- Output:
			- Outputs a pointer to a clone of the GraphicalObject.

Classe GraphicalObject:
É uma classe puramente virtual que é pai de todos os outros objetos gráficos.
	- Destrutor:
		- É o destrutor padrão do C++. É usado em todas as classes filhas.
	- has_point:
		- Entrada:
			- p: Um ponto.
		- Saída:
			- Retorna True se o GraphicalObject contém o ponto ou False caso
contrário.
	- boundingBox:
		- Saída:
			- Retorna uma  estrutura Rect com o menor retângulo envolvente que
contém todos os pontos do GraphicalObject.
	- clone:
		- Saída:
			- Retorna um ponteiro para um clone do GraphicalObject.
*/
class GraphicalObject {
public:
	virtual ~GraphicalObject () {}
	virtual bool has_point (const Point& p) const = 0;
	virtual Rect boundingBox () const = 0;
	virtual GraphicalObject *clone () const = 0;
};

/*
Circle class:
Child class of GraphicalObject. Stores the center, the radius and the thickness
of a circunference.
	- Constructor:
		- center: The point that will be the center of the circle;
		- thick: The thickness of the circle in units;
		- radius: The radius of the circle in units.
	- get_thick:
		- A debugging function that prints the thickness of the circle.

Classe Circle:
Classe filha da GraphicalObject. Guarda o centro, o raio e a grossura de uma
circunferência.
	- Construtor:
		- center: O ponto que será o centro do círculo;
		- thick: A grossura do círculo em unidades;
		- raduis: O raio do círculo em unidades.
	- get_thick:
		- Uma função para debug que imprime a grossura do círculo.
*/
class Circle : public GraphicalObject {
	Point center;
	double radius, thick;
public:
	Circle (const Point& center, double radius, double thick):
		center(center), thick(thick), radius(radius) {}
	bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new Circle(*this));
	}
	void get_thick () {
		std::cout << thick << std::endl;
	}
};

/*
Line class:
Child class of GraphicalObject. Stores the vertices and the thickness of a line.
	- Constructor:
		- p1: The first vertice;
		- p2: The second vertice;
		- thick: The thickness of the line.

Classe Line:
Classe filha da GraphicalObject. Guarda os vértices e a grossura de uma linha.
	- Construtor:
		- p1: O primeiro vértice;
		- p2: O segundo vértice;
		- thick: A grossura da linha.
*/
class Line : public GraphicalObject {
	Point p1, p2;
	double thick;
public:
	Line (const Point& p1, const Point& p2, double thick):
		p1(p1), p2(p2), thick(thick) {}
	bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new Line(*this));
	}
};

/*
Group class:
Child class of GraphicalObject. Conteins a list of pointers to other graphical
objects.
	- Constructor:
		- Can be created without parameters, creating an empty group, or can be
created using another Group as parameter, in this case it's the same as cloning
it.
	- add:
		Adds a GraphicalObject to the group.
		- Input:
			- obj: The object that will be added to the group.

Classe Group:
Classe filha da GraphicalObject. Contém uma lista de ponteiros para outros
objetos gráficos.
	- Construtor:
		- Pode ser criado sem parâmetros, criando um grupo vazio, ou pode ser
criado usando outro grupo como parâmetro, nesse caso seria o mesmo que clonar o
grupo usado como parâmetro.
	- add:
		Adiciona um GraphicalObject ao grupo.
		- Entrada:
			- obj: O objeto que será adicionado ao grupo.
*/
class Group : public GraphicalObject {
	struct Node {
		GraphicalObject *obj;
		struct Node *next;
	};
	Node *Head;
public:
	Group(): Head(NULL) {}
	Group(const Group& other);
	~Group();
	void add (const GraphicalObject& obj);
	bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new Group(*this));
	}
};

/*
Polygon class:
Child class of GraphicalObject. It's an array of points conected with lines.
The first point of the array is connected with the last point.
	- Constructor:
		- filled: It's a bool variable that tells if the inner part of the
polygon will be collored.
		- thick: A double variable that controls the thickness of the edges of
the polygon in units.
		- other: An optional parameter that, if present, creates a copy of the
provided polygon.
	- add:
		- pt: Add the point pt to the array of the polygon.

Classe Polygon:
Classe filha da GraphicalObject. Contém uma lista de pontos conectados por
linhas. O primeiro ponto da lista é conectado com o último.
	- Construtor:
		- filled: É uma variável booleana que diz se a parte interna do polígono
será colorida.
		- thick: Uma variável double que controla a grossura das arestas do
polígono em unidades.
		- other: Um parâmetro opcional que, se presente, cria uma cópia do
polígono fornecido.
	- add:
		- pt: Adiciona o ponto pt à lista do polígono.
*/
class Polygon : public GraphicalObject {
	struct Node {
		Point *pt;
		struct Node *next;
	};
	Node *Head;
	bool filled;
	double thick;
public:
	Polygon (bool filled, double thick): Head(NULL), filled(filled), thick(thick) {}
	Polygon (const Polygon& other, bool filled, double thick);
	~Polygon ();
	void add (const Point& pt);
	virtual bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new Polygon(*this));
	}
};

/*
LineArray class:
Child class of GraphicalObject. It's an array of points conected with lines.
The first point of the array is not connected with the last point.
	- Constructor:
		- thick: A double variable that controls the thickness of the edges of
the lines in units.
		- other: An optional parameter that, if present, creates a copy of the
provided LineArray.
	- add:
		- pt: Add the point pt to the array.

Classe LineArray:
Classe filha da GraphicalObject. Contém uma lista de pontos conectados por
linhas. O primeiro ponto da lista não é conectado com o último.
	- Construtor:
		- thick: Uma variável double que controla a grossura das linhas em
unidades.
		- other: Um parâmetro opcional que, se presente, cria uma cópia do
LineArray fornecido.
	- add:
		- pt: Adiciona o ponto pt à lista.
*/
class LineArray : public GraphicalObject {
	struct Node {
		Point *pt;
		struct Node *next;
	};
	Node *Head;
	double thick;
public:
	LineArray (double thick): Head(NULL), thick(thick) {}
	LineArray (const LineArray& other, double thick);
	void add (const Point& pt);
	bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new LineArray(*this));
	}
};

/*
RegularPolygon class:
Child class of GraphicalObject. Creates a regular polygon with some number of
sides centered in some point.
	- Constructor:
		- center: It's the point which the polygon will be centered.
		- sides: The number of sides of the polygon.
		- size: It's the radius of the circle thar circunscribes the polygon.
		- thick: A double varible that tells the thickness of the edges of the
polygon.

Classe RegularPolygon:
Classe filha da GraphicalObject. Cria um polígono regular com certo número de
lados, cetrado em algum ponto.
	- Construtor:
		- center: É o ponto em que o polígono será centrado.
		- sides: O número de lados do polígono.
		- size: É o raio do círculo que circunscreve o polígono.
		- thick: Uma variável double que diz qual a grossura das arestas do
polígono.
*/
class RegularPolygon : public GraphicalObject {
	struct Node {
		Point *pt;
		struct Node *next;
	};
	Node *Head;
	Point center;
	double thick, size;
	int sides;
public:
	RegularPolygon (const Point& center, int sides, double size, double thick);
	RegularPolygon (const RegularPolygon& other);
	bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new RegularPolygon(*this));
	}
};

/*
Ellipse class:
Child class of GraphicalObject. Draws an ellipse.
	- Constructor:
		- center: The point which the ellipse will be centered.
		- angle: The angle which the ellipse is rotated.
		- a: The major axis of the ellipse.
		- b: The minnor axis of the ellipse.
		- thick: The thickness of the ellipse's borders in units.

Classe Ellipse:
Classe filha da GraphicalObject. Desenha uma elipse.
	- Construtor:
		- center: O ponto em que a elipse será centrada.
		- angle: O ângulo de rotação da elipse.
		- a: O eixo maior da elipse.
		- b: O eixo menor da elipse.
		- thick: A grossura das brodas da elipse em unidades.
*/
class Ellipse : public GraphicalObject {
	Point f1, f2, center;
	double a, b, angle, thick;
public:
	Ellipse (const Point& center, double angle, double a, double b, double thick):
		center(center), angle(angle), a(a), b(b), thick(thick) {
		double recoilx = sqrt(fabs(sq(a)-sq(b)))*cos(angle);
		double recoily = sqrt(fabs(sq(a)-sq(b)))*sin(angle);
		f1 = Point(center.x+recoilx, center.y+recoily);
		f2 = Point(center.x-recoilx, center.y-recoily);
	}
	Ellipse (const Ellipse& other);
	bool has_point (const Point& p) const;
	Rect boundingBox () const;
	GraphicalObject *clone () const {
		return (new Ellipse(*this));
	}
};

#endif
