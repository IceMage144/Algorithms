#include "polygons.h"
#include "pgmdrawer.h"
#include <iostream>

using namespace std;

/*
This is the main file for testing the functions.

Esse é o arquivo principal para testar as funções.
*/

int main () {
	Point pt1(10,10);
	Point pt2(8,7);
	Point pt3(3,0);
	Point pt4(1,8);
	Group G;
	LineArray P(1, 0.1);
	P.add(pt1);
	P.add(pt2);
	P.add(pt3);
	P.add(pt4);
	Circle circ(pt1, 3, 0.1);
	Circle circ2(pt2, 3, 0.1);
	Line line(pt1, pt2, 0.1);
	Line line2(pt1, pt4, 0.1);
	G.add(circ);
	G.add(circ2);
	G.add(line);
	G.add(line2);
	RegularPolygon S(pt3, 3, 5, 0.1);
	Ellipse E(pt1, 0, 2, 4, 1);
	Rect box = S.boundingBox();
	cout << box.llc.x << ", " << box.llc.y << ":";
	cout << box.urc.x << ", " << box.urc.y << endl;
	FILE *f = fopen("image.pgm", "w");
	Canvas c;
	c.save_pgm(E, f, 20, 5);
	fclose(f);
	return 0;
}
