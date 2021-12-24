
from lib.Math.Vector import Vector2 as V
from itertools import combinations

def list_all_triangles(points):
    return list(combinations(points, 3))