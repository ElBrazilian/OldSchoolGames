
from lib.Math.Vector import Vector2 as V
from itertools import combinations

def list_all_triangles(points):
    return list(combinations(points, 3))

def point_in_triangle(p, a, b, c):
    p, a, b, c = V(p), V(a), V(b), V(c)
    def sign(a,b,c):
        return (a.x - c.x)*(b.y-c.y)-(b.x-c.x)*(a.y-c.y)

    d1 = sign(p,a,b)
    d2 = sign(p,b,c)
    d3 = sign(p,c,a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)