#include <cstdio>
#include "pgmdrawer.h"
#include "polygons.h"

/*
Implementing the method save_pgm from Canvas.

Implementando o método save_pgm do Canvas.
*/

bool Canvas::save_pgm (const GraphicalObject& obj, FILE *output,
					int pix_per_unit, int sample_size) const {
	double pix_size = 1.0/pix_per_unit;
	double eps = pix_size/(sample_size+1);
	Rect box = obj.boundingBox();
	int width = pix_per_unit*(box.urc.x-box.llc.x)+1;
	int height = pix_per_unit*(box.urc.y-box.llc.y)+1;
	fprintf(output, "P2\n");
	fprintf(output, "%d %d\n", width, height);
	fprintf(output, "255\n");
	for (int h = height-1; h >= 0; h--) {
		for (int w = 0; w < width; w++) {
			double x0 = box.llc.x + w*pix_size;
			double y0 = box.llc.y + h*pix_size;
			int total = sample_size*sample_size;
			for (int i = 1; i <= sample_size; i++)
				for (int j = 1; j <= sample_size; j++)
					if (obj.has_point(Point(x0+i*eps, y0+j*eps)))
						total--;
			fprintf(output, "%d ", 255*total/sample_size/sample_size);
		}
		fprintf(output, "\n");
	}
	return true;
}
