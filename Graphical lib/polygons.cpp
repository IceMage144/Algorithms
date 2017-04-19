#include "polygons.h"
#include <cmath>
#include <iostream>

/*
In this file, the rest of the methods from polygons.h are implemented.

Nesse arquivo são implementados os métodos do polygons.h que sobraram.
*/

using namespace std;

double sq (double x) {
	return x*x;
}

bool areIntersecting (const Point& v1p1, const Point& v1p2, const Point& v2p1, const Point& v2p2) {
	double a1, b1, c1, d1, d2, a2, b2, c2, d3, d4;
	a1 = v1p1.y-v1p2.y;
	b1 = v1p1.x-v1p2.y;
	c1 = v1p1.y*v1p2.x - v1p1.x*v1p2.y;
	d1 = a1*v2p1.x + b1*v2p1.y + c1;
	d2 = a1*v2p2.x + b1*v2p2.y + c1;
	a2 = v2p1.y-v2p2.y;
	b2 = v2p1.x-v2p2.y;
	c2 = v2p1.y*v2p2.x - v2p1.x*v2p2.y;
	d3 = a2*v1p1.x + b2*v1p1.y + c2;
	d4 = a1*v1p2.x + b1*v1p2.y + c1;
	if ((d1 < 0 && d2 > 0) || (d1 > 0 && d2 < 0))
		if ((d3 < 0 && d4 > 0) || (d3 > 0 && d4 < 0))
			return true;
	return false;
}

bool Circle::has_point (const Point& p) const {
	double dist1 = sq(radius+thick);
	double dist2 = sq(radius-thick);
	double distpt = sq(p.x-center.x) + sq(p.y-center.y);
	if (distpt <= dist1 && distpt >= dist2)
		return true;
	return false;
}

Rect Circle::boundingBox () const {
	Rect box;
	box.llc.x = center.x - radius - thick;
	box.llc.y = center.y - radius - thick;
	box.urc.x = center.x + radius + thick;
	box.urc.y = center.y + radius + thick;
	return box;
}

bool Line::has_point (const Point& p) const {
	double t = min(sqrt((p.x-p1.x)*(p.x-p1.x)+(p.y-p1.y)*(p.y-p1.y)), sqrt((p.x-p2.x)*(p.x-p2.x)+(p.y-p2.y)*(p.y-p2.y)));
	if (t <= thick)
		return true;
	Point vec1(p1.x-p2.x, p1.y-p2.y);
	Point vec2(p1.x-p.x, p1.y-p.y);
	double frac = (vec1.x*vec2.x + vec1.y*vec2.y)/(vec1.x*vec1.x + vec1.y*vec1.y);
	if (frac < 0 || frac > 1)
		return false;
	Point vec3(vec1.x*frac, vec1.y*frac);
	t = sqrt((vec2.x*vec2.x + vec2.y*vec2.y) - (vec3.x*vec3.x + vec3.y*vec3.y));
	if (t <= thick)
		return true;
	return false;
}

Rect Line::boundingBox () const {
	Rect box;
	box.llc.x = fmin(p1.x, p2.x)-thick;
	box.llc.y = fmin(p1.y, p2.y)-thick;
	box.urc.x = fmax(p1.x, p2.x)+thick;
	box.urc.y = fmax(p1.y, p2.y)+thick;
	return box;
}

Group::Group (const Group& other): Head(NULL) {
	for (Node *cell = other.Head; cell != NULL; cell = cell->next) {
		add(*cell->obj);
	}
}

Group::~Group () {
	for (Node *temp, *cell = Head; cell != NULL; cell = temp) {
		temp = cell->next;
		delete cell->obj;
		delete cell;
	}
}

void Group::add (const GraphicalObject& obj) {
	Node *cell = new Node;
	cell->obj = obj.clone();
	cell->next = Head;
	Head = cell;
}

bool Group::has_point (const Point& p) const {
	for (Node *cell = Head; cell != NULL; cell = cell->next)
		if (cell->obj->has_point(p)) {
			//printf("%p have (%f, %f)\n", cell, p.x, p.y);
			return true;
		}
	//printf("I do not have (%f, %f)\n", p.x, p.y);
	return false;
}

Rect Group::boundingBox () const {
	Rect box, aux;
	for (Node *cell = Head; cell != NULL; cell = cell->next) {
		aux = cell->obj->boundingBox();
		if(aux.llc.x < box.llc.x)
            box.llc.x = aux.llc.x;
        if(aux.llc.y < box.llc.y)
            box.llc.y = aux.llc.y;
        if(aux.urc.x > box.urc.x)
            box.urc.x = aux.urc.x;
        if(aux.urc.y > box.urc.y)
            box.urc.y = aux.urc.y;
	}
	return box;
}

Polygon::Polygon (const Polygon& other, bool filled, double thick):
	filled(filled), thick(thick) {
	for (Node *cell = other.Head; cell != NULL; cell = cell->next) {
		add(*cell->pt);
	}
}

Polygon::~Polygon () {
	for (Node *temp, *cell = Head; cell != NULL; cell = temp) {
		temp = cell->next;
		delete cell->pt;
		delete cell;
	}
}

void Polygon::add (const Point& pt) {
	Node *cell = new Node;
	cell->pt = new Point(pt.x, pt.y);
	cell->next = Head;
	Head = cell;
}

bool Polygon::has_point (const Point& p) const {
	if (Head == NULL)
		return false;
	Node *cell = Head;
	for (Node *cell2 = Head->next; cell2 != NULL; cell = cell2, cell2 = cell2->next) {
		Line line(*cell->pt, *cell2->pt, thick);
		if (line.has_point(p))
			return true;
	}
	Line line(*cell->pt, *Head->pt, thick);
	if (line.has_point(p))
		return true;
	if (filled == true) {
		Rect box = boundingBox();
		Point raypt1(box.llc.x, p.y);
		Point raypt2(p.x, p.y);
		int count = 0;
		cell = Head;
		for (Node *cell2 = Head->next; cell2 != NULL; cell = cell2, cell2 = cell2->next) {
			if (areIntersecting(*cell->pt, *cell2->pt, raypt1, raypt2))
				count++;
		}
		if (areIntersecting(*cell->pt, *Head->pt, raypt1, raypt2))
			count++;
		if (count%2)
			return true;
		return false;
	}
}

Rect Polygon::boundingBox () const {
	Rect box;
	for (Node *cell = Head; cell != NULL; cell = cell->next) {
		if(cell->pt->x < box.llc.x)
            box.llc.x = cell->pt->x;
        if(cell->pt->y < box.llc.y)
            box.llc.y = cell->pt->y;
        if(cell->pt->x > box.urc.x)
            box.urc.x = cell->pt->x;
        if(cell->pt->y > box.urc.y)
            box.urc.y = cell->pt->y;
	}
	return box;
}

void LineArray::add (const Point& pt) {
	Node *cell = new Node;
	cell->pt = new Point(pt.x, pt.y);
	cell->next = Head;
	Head = cell;
}

LineArray::LineArray (const LineArray& other, double thick):
	thick(thick), Head(NULL) {
	for (Node *cell = other.Head; cell != NULL; cell = cell->next) {
		add(*(cell->pt));
	}
}

bool LineArray::has_point (const Point& p) const {
	if (Head == NULL)
		return false;
	Node *cell = Head;
	for (Node *cell2 = Head->next; cell2 != NULL; cell = cell2, cell2 = cell2->next) {
		Line line(*cell->pt, *cell2->pt, thick);
		if (line.has_point(p))
			return true;
	}
}

Rect LineArray::boundingBox () const {
	Rect box;
	for (Node *cell = Head; cell != NULL; cell = cell->next) {
		if(cell->pt->x < box.llc.x)
            box.llc.x = cell->pt->x;
        if(cell->pt->y < box.llc.y)
            box.llc.y = cell->pt->y;
        if(cell->pt->x > box.urc.x)
            box.urc.x = cell->pt->x;
        if(cell->pt->y > box.urc.y)
            box.urc.y = cell->pt->y;
	}
	return box;
}

RegularPolygon::RegularPolygon (const Point& center, int sides, double size, double thick):
	sides(sides), size(size), thick(thick), center(center), Head(NULL) {
	Node *cell;
	double angle = 0;
	for (int i = 0; i < sides; i++) {
		cell = new Node;
		cell->pt = new Point(center.x + size*cos(angle), center.y + size*sin(angle));
		cell->next = Head;
		Head = cell;
		angle += TAU/sides;
		cout << "(" << center.x*cos(angle) << ", " << center.y*sin(angle) << ")" << endl;
	}
}

RegularPolygon::RegularPolygon (const RegularPolygon& other):
	Head(NULL) {
	Node *aux;
	for (Node *cell = other.Head; cell != NULL; cell = cell->next) {
		aux = new Node;
		aux->pt = new Point(cell->pt->x, cell->pt->y);
		aux->next = Head;
		Head = aux;
	}
	sides = other.sides;
	size = other.size;
	thick = other.thick;
	center = Point(other.center.x, other.center.y);
}

bool RegularPolygon::has_point (const Point& p) const {
	if (Head == NULL)
		return false;
	Node *cell = Head;
	for (Node *cell2 = Head->next; cell2 != NULL; cell = cell2, cell2 = cell2->next) {
		//cout << "(" << cell2->pt->x << ", " << cell2->pt->y << ")" << endl;
		Line line(*cell->pt, *cell2->pt, thick);
		if (line.has_point(p))
			return true;
	}
	Line line(*cell->pt, *Head->pt, thick);
	if (line.has_point(p))
		return true;
}

Rect RegularPolygon::boundingBox () const {
	Rect box;
	for (Node *cell = Head; cell != NULL; cell = cell->next) {
		if(cell->pt->x < box.llc.x)
            box.llc.x = cell->pt->x;
        if(cell->pt->y < box.llc.y)
            box.llc.y = cell->pt->y;
        if(cell->pt->x > box.urc.x)
            box.urc.x = cell->pt->x;
        if(cell->pt->y > box.urc.y)
            box.urc.y = cell->pt->y;
	}
	return box;
}

Ellipse::Ellipse (const Ellipse& other) {
	f1 = Point(other.f1.x, other.f1.y);
	f2 = Point(other.f2.x, other.f2.y);
	center = Point(other.center.x, other.center.y);
	angle = other.angle;
	thick = other.thick;
	a = other.a;
	b = other.b;
}

bool Ellipse::has_point (const Point& p) const {
	/*double distfbf1 = 2*max(a,b)-thick; //Sum of the distance of the focuses to the border minus thick
	double distfbf2 = 2*max(a,b)+thick; //Sum of the distance of the focuses to the border plus thick
	double distfpf = sqrt(sq(f1.x-p.x)+sq(f1.y-p.y)) + sqrt(sq(f2.x-p.x)+sq(f2.y-p.y)); //Sum of the distance of the focuses to the point
	if (distfpf >= distfbf1 && distfpf <= distfbf2)
		return true;
	return false;*/
	double xcoord = (p.x-center.x)*cos(angle)-(p.y-center.y)*sin(angle);
	double ycoord = (p.x-center.x)*sin(angle)+(p.y-center.y)*cos(angle);
	double val1 = sq(xcoord/(a-thick/2)) + sq(ycoord/(b-thick/2));
	double val2 = sq(xcoord/(a+thick/2)) + sq(ycoord/(b+thick/2));
	if (val1 >= 1 && val2 <= 1)
		return 1;
	return 0;
}

Rect Ellipse::boundingBox () const {
	Rect box;
	double varx = sq(a*sin(angle))+sq(b*cos(angle));
	double vary = sq(a*cos(angle))+sq(b*sin(angle));
	varx = a*b/sqrt(varx) + fabs(sin(2*angle))*min(a,b)/max(a,b);
	vary = a*b/sqrt(vary) + fabs(sin(2*angle))*min(a,b)/max(a,b);
	box.llc.x = center.x - varx - thick;
	box.llc.y = center.y - vary - thick;
	box.urc.x = center.x + varx + thick;
	box.urc.y = center.y + vary + thick;
	return box;
}
