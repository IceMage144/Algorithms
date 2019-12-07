import math
from random import random
import matplotlib.pyplot as plt

box = (5, 5)
objects = (((1, -0.5), (0, 2), (-1, -0.5)),
           ((-1, 0.5), (0, -2), (1, 0.5)))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            self.x *= other
            self.y *= other
            return self
        return self.x*other.x + self.y*other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    __repr__ = __str__

    def plot(self):
        plt.plot(self.x, self.y)

class Line:
    def __init__(self, alpha, beta, gamma=None):
        if type(alpha) == Point:
            p1 = alpha
            p2 = beta
            alpha = p2.y - p1.y
            beta = p1.x - p2.x
            gamma = p2.x*p1.y - p1.x*p2.y
        norm_factor = 1.0/math.sqrt(alpha**2 + beta**2)
        self.alpha = alpha * norm_factor
        self.beta = beta * norm_factor
        self.gamma = gamma * norm_factor

    def __str__(self):
        return f"({self.alpha}, {self.beta}, {self.gamma})"

    __repr__ = __str__

    def dist_to_point(self, p):
        return self.alpha*p.x + self.beta*p.y + self.gamma

class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []
        self.original_gammas = []
        self._offset = Point(0, 0)
        for i in range(len(vertices) - 1):
            line = Line(vertices[i], vertices[i+1])
            self.edges.append(line)
            self.original_gammas.append(line.gamma)
        line = Line(vertices[-1], vertices[0])
        self.edges.append(line)
        self.original_gammas.append(line.gamma)

    def __str__(self):
        return f"Polygon:\n\toffset = {self.offset}\n\tvertices = {self.vertices}\n\tedges = {self.edges}\n\tgammas = {self.original_gammas}"

    __repr__ = __str__

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, new_offset):
        for edge, gamma in zip(self.edges, self.original_gammas):
            edge.gamma = gamma - edge.alpha*new_offset.x - edge.beta*new_offset.y
        for i in range(len(self.vertices)):
            self.vertices[i] += new_offset - self._offset
        self._offset = new_offset

    def plot(self):
        for v1,v2 in zip(self.vertices, self.vertices[1:]):
            (v1 + self.offset).plot()
            plt.plot([v1.x, v2.x],
                     [v1.y, v2.y])
        self.vertices[-1].plot()
        plt.plot([self.vertices[-1].x, self.vertices[0].x],
                 [self.vertices[-1].y, self.vertices[0].y])


def polygon_dist(pol1, pol2):
    mx = float("-inf")
    mx_idx = 0
    pol = 1
    for i, e in enumerate(pol1.edges):
        mn = float("inf")
        for j, v in enumerate(pol2.vertices):
            d = e.dist_to_point(v)
            print(d)
            mn = min(mn, d)
        if mn > mx:
            mx = mn
            mx_idx = i
        print(f"min: {mn}")
    print("--------")
    for i, e in enumerate(pol2.edges):
        mn = float("inf")
        for j, v in enumerate(pol1.vertices):
            d = e.dist_to_point(v)
            print(d)
            mn = min(mn, d)
        if mn > mx:
            mx = mn
            mx_idx = i
            pol = 2
        print(f"min: {mn}")
    print((mx, pol, mx_idx))
    return (mx, pol, mx_idx)

def get_boundary_polygon(box):
    boundary_vertices = [(0, 0), (0, box[1]), (box[0], box[1]), (box[0], 0)]
    return Polygon([Point(*v) for v in boundary_vertices])

def uncollide(polygons):
    mn = -1
    while mn < 0:
        mn = float("inf")
        for pol1 in polygons:
            for pol2 in polygons:
                if pol1 == pol2:
                    continue
                d, pol, idx = polygon_dist(pol1, pol2)
                if d < 0:
                    pol = pol1 if pol == 1 else pol2
                    other_pol = pol2 if pol == 1 else pol1
                    edge = pol.edges[idx]
                    other_pol.offset -= Point(edge.alpha, edge.beta)*d
                    print(polygons)
                mn = min(mn, d)
        print(mn)

def main():
    polygons = [get_boundary_polygon(box)]
    for object in objects:
        poly = Polygon([Point(*v) for v in object])
        poly.offset = Point(box[0]*random(), box[1]*random())
        polygons.append(poly)

    print(polygons)
    uncollide(polygons)

    boundary = polygons[0]
    boundary.plot()
    positions = []
    for pol in polygons[1:]:
        positions.append(pol.offset - boundary.offset)
        pol.plot()
    print(positions)

    plt.show()


if __name__ == '__main__':
    main()
